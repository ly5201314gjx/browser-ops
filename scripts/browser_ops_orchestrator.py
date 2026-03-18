#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime

from state_store import load_json, save_json
from profile_runner import load_profile


def _effective_route(orch: dict) -> str:
    intel = orch.get("intelligence", {})
    return intel.get("recommendedRoute") or orch.get("route", "browser")


def init_run(profile_path: str, task_dir: str, detail_limit: int = 5, page_limit: int | None = None, intelligence_first: bool = True) -> dict:
    profile = load_profile(profile_path)
    td = Path(task_dir)
    td.mkdir(parents=True, exist_ok=True)
    run = {
        "createdAt": datetime.now().isoformat(),
        "profilePath": str(Path(profile_path).resolve()),
        "taskDir": str(td.resolve()),
        "profile": profile.get("name"),
        "route": profile.get("route", "browser"),
        "status": "initialized",
        "pageLimit": page_limit or profile.get("maxPages", 1),
        "detailLimit": detail_limit,
        "currentPhase": "intelligence" if intelligence_first else "list",
        "nextAction": "open_start_url_for_intelligence" if intelligence_first else "open_start_url",
        "startUrl": profile.get("startUrls", [""])[0],
        "listPagesCompleted": 0,
        "detailsCompleted": 0,
        "notes": [],
    }
    save_json(str(td / "orchestrator_state.json"), run)
    return run


def status(task_dir: str) -> dict:
    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    batch = load_json(str(td / "detail_batch_state.json"), default={})
    return {
        "ok": True,
        "effectiveRoute": _effective_route(orch),
        "orchestrator": orch,
        "browserRuntime": runtime,
        "detailBatch": batch,
    }


def next_action(task_dir: str) -> dict:
    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    batch = load_json(str(td / "detail_batch_state.json"), default={})

    phase = orch.get("currentPhase", "list")
    effective_route = _effective_route(orch)
    intel = orch.get("intelligence", {})

    if phase == "intelligence":
        if not intel:
            return {
                "ok": True,
                "phase": "intelligence",
                "action": "open_url",
                "url": orch.get("startUrl", ""),
                "instruction": "Open the start URL, snapshot it, save to bootstrap-snapshot.txt, then run intelligence_bootstrap.py"
            }
        orch["currentPhase"] = "list"
        orch["nextAction"] = "open_start_url"
        save_json(str(td / "orchestrator_state.json"), orch)
        return {
            "ok": True,
            "phase": "list",
            "action": "resume_list",
            "effectiveRoute": effective_route,
            "instruction": "Intelligence bootstrap complete. Continue with list workflow using the recommended route/profile hints."
        }

    if phase == "list":
        if effective_route == "human":
            return {
                "ok": True,
                "phase": "list",
                "action": "human_checkpoint",
                "effectiveRoute": effective_route,
                "instruction": "Human checkpoint required by intelligence result. Do not automate past the protection wall; ask for user help and capture artifacts."
            }

        if effective_route == "http":
            return {
                "ok": True,
                "phase": "list",
                "action": "http_route",
                "effectiveRoute": effective_route,
                "instruction": "Use the HTTP route for this site. Run crawl_orchestrator.py or http_crawler.py with the profile/task dir."
            }

        visited = runtime.get("pagesVisited", 0)
        next_url = runtime.get("suggestedNextUrl", "")
        page_limit = orch.get("pageLimit", 1)

        if visited == 0:
            return {
                "ok": True,
                "phase": "list",
                "action": "open_url",
                "effectiveRoute": effective_route,
                "url": orch.get("startUrl", ""),
                "instruction": "Open the start URL, snapshot it, save to page1.txt, then run browser_page_processor.py"
            }

        if visited < page_limit and next_url:
            return {
                "ok": True,
                "phase": "list",
                "action": "open_url",
                "effectiveRoute": effective_route,
                "url": next_url,
                "instruction": f"Open next page ({next_url}), snapshot it, save to page{visited+1}.txt, then run browser_page_processor.py"
            }

        orch["currentPhase"] = "detail-queue"
        orch["nextAction"] = "build_detail_queue"
        save_json(str(td / "orchestrator_state.json"), orch)
        return {
            "ok": True,
            "phase": "detail-queue",
            "action": "build_detail_queue",
            "effectiveRoute": effective_route,
            "instruction": "List phase complete. Build detail queue with detail_queue_builder.py and init detail_batch_driver.py"
        }

    if phase == "detail-queue":
        return {
            "ok": True,
            "phase": "detail-queue",
            "action": "build_detail_queue",
            "effectiveRoute": effective_route,
            "instruction": "Run detail_queue_builder.py and detail_batch_driver.py init, then set phase to detail and ask for next_action again"
        }

    if phase == "detail":
        idx = batch.get("currentIndex", 0)
        items = batch.get("items", [])
        if idx >= len(items):
            orch["currentPhase"] = "report"
            orch["nextAction"] = "build_report"
            save_json(str(td / "orchestrator_state.json"), orch)
            return {
                "ok": True,
                "phase": "report",
                "action": "build_report",
                "effectiveRoute": effective_route,
                "instruction": "Detail phase complete. Rebuild report."
            }
        item = items[idx]
        return {
            "ok": True,
            "phase": "detail",
            "action": "open_detail_url",
            "effectiveRoute": effective_route,
            "url": item.get("link", ""),
            "item": item,
            "instruction": "Open detail URL, snapshot it, save to detail-N.txt, run browser_detail_processor.py, then mark done/fail in detail_batch_driver.py"
        }

    if phase == "report":
        return {
            "ok": True,
            "phase": "report",
            "action": "build_report",
            "effectiveRoute": effective_route,
            "instruction": "Run report_builder.py and finish the task"
        }

    return {"ok": False, "error": f"unknown phase: {phase}"}


def advance_phase(task_dir: str, phase: str) -> dict:
    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    orch["currentPhase"] = phase
    orch["nextAction"] = "pending"
    save_json(str(td / "orchestrator_state.json"), orch)
    return orch


def append_note(task_dir: str, note: str) -> dict:
    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    orch.setdefault("notes", []).append({"ts": datetime.now().isoformat(), "note": note})
    save_json(str(td / "orchestrator_state.json"), orch)
    return orch


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: browser_ops_orchestrator.py <init|status|next|phase|note> ...", file=sys.stderr)
        return 1
    cmd = argv[1]
    if cmd == "init":
        if len(argv) < 4:
            print("Usage: browser_ops_orchestrator.py init <profile.json> <task_dir> [detail_limit] [page_limit] [intelligence_first]", file=sys.stderr)
            return 1
        detail_limit = int(argv[4]) if len(argv) > 4 else 5
        page_limit = int(argv[5]) if len(argv) > 5 else None
        intelligence_first = (argv[6].lower() != "false") if len(argv) > 6 else True
        print(json.dumps(init_run(argv[2], argv[3], detail_limit, page_limit, intelligence_first), ensure_ascii=False))
        return 0
    if cmd == "status":
        print(json.dumps(status(argv[2]), ensure_ascii=False, indent=2))
        return 0
    if cmd == "next":
        print(json.dumps(next_action(argv[2]), ensure_ascii=False, indent=2))
        return 0
    if cmd == "phase":
        print(json.dumps(advance_phase(argv[2], argv[3]), ensure_ascii=False))
        return 0
    if cmd == "note":
        print(json.dumps(append_note(argv[2], argv[3]), ensure_ascii=False))
        return 0
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
