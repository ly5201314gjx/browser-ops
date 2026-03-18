#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from state_store import load_json, save_json


def _next_page_filename(task_dir: Path, page_num: int) -> str:
    return str(task_dir / f"page{page_num}.txt")


def _next_detail_filename(task_dir: Path, detail_num: int) -> str:
    return str(task_dir / f"detail-{detail_num:03d}.txt")


def _effective_route(orch: dict) -> str:
    intel = orch.get("intelligence", {})
    return intel.get("recommendedRoute") or orch.get("route", "browser")


def build_runbook(task_dir: str) -> dict:
    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    batch = load_json(str(td / "detail_batch_state.json"), default={})
    action_policy = load_json(str(td / "action_policy.json"), default={})

    phase = orch.get("currentPhase", "list")
    effective_route = _effective_route(orch)
    interaction = action_policy.get("interactionPolicy", {})
    runbook = {
        "taskDir": str(td),
        "phase": phase,
        "effectiveRoute": effective_route,
        "actionPolicy": {
            "device": action_policy.get("device"),
            "navigationStyle": action_policy.get("navigationStyle"),
            "riskTolerance": action_policy.get("riskTolerance"),
            "checkpointPolicy": action_policy.get("checkpointPolicy", {}),
            "interactionPolicy": interaction,
        },
        "steps": [],
    }

    if phase == "intelligence":
        start_url = orch.get("startUrl", "")
        target_file = str(td / "bootstrap-snapshot.txt")
        runbook["headline"] = "Intelligence bootstrap"
        runbook["steps"] = [
            {"kind": "browser.open", "url": start_url, "settleMs": interaction.get("timing", {}).get("pageSettleMs", [1200, 3200])},
            {"kind": "browser.snapshot", "saveTo": target_file, "pauseBeforeMs": interaction.get("timing", {}).get("elementConfirmPauseMs", [300, 900])},
            {
                "kind": "exec",
                "command": f"python3 skills/browser-ops/scripts/intelligence_bootstrap.py {td} {target_file} {start_url}"
            }
        ]
        return runbook

    if phase == "list":
        if effective_route == "human":
            current_url = runtime.get('lastUrl') or orch.get('startUrl', '')
            runbook["headline"] = "Human checkpoint required"
            runbook["steps"] = [
                {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/handoff_packet.py build {td} protected-checkpoint '{current_url}' '' ''"},
                {"kind": "note", "text": "Do not automate through the protection wall."},
                {"kind": "note", "text": "Ask the human to complete the blocked step, then resume with handoff_packet.py resume."},
            ]
            return runbook

        if effective_route == "http":
            runbook["headline"] = "Use HTTP route"
            runbook["steps"] = [
                {
                    "kind": "exec",
                    "command": f"python3 skills/browser-ops/scripts/crawl_orchestrator.py {orch.get('profilePath')} {td}"
                }
            ]
            return runbook

        visited = runtime.get("pagesVisited", 0)
        next_url = runtime.get("suggestedNextUrl", "")
        if visited == 0:
            start_url = orch.get("startUrl", "")
            target_file = _next_page_filename(td, 1)
            runbook["headline"] = "Process first list page"
            runbook["steps"] = [
                {"kind": "browser.open", "url": start_url, "settleMs": interaction.get("timing", {}).get("pageSettleMs", [1200, 3200])},
                {"kind": "browser.snapshot", "saveTo": target_file, "pauseBeforeMs": interaction.get("timing", {}).get("elementConfirmPauseMs", [300, 900])},
                {
                    "kind": "exec",
                    "command": f"python3 skills/browser-ops/scripts/browser_page_processor.py {td} {target_file} {start_url} 'page 1 processed'"
                },
                {
                    "kind": "exec",
                    "command": f"python3 skills/browser-ops/scripts/artifact_recorder.py artifact {td} snapshot {target_file} {start_url} 'page 1 snapshot'"
                },
            ]
            return runbook

        if next_url:
            page_num = visited + 1
            target_file = _next_page_filename(td, page_num)
            runbook["headline"] = f"Process list page {page_num}"
            runbook["steps"] = [
                {"kind": "browser.navigate", "url": next_url, "scrollPauseMs": interaction.get("motion", {}).get("postScrollPauseMs", [250, 900])},
                {"kind": "browser.snapshot", "saveTo": target_file, "pauseBeforeMs": interaction.get("timing", {}).get("elementConfirmPauseMs", [300, 900])},
                {
                    "kind": "exec",
                    "command": f"python3 skills/browser-ops/scripts/browser_page_processor.py {td} {target_file} '{next_url}' 'page {page_num} processed'"
                },
                {
                    "kind": "exec",
                    "command": f"python3 skills/browser-ops/scripts/artifact_recorder.py artifact {td} snapshot {target_file} '{next_url}' 'page {page_num} snapshot'"
                },
            ]
            return runbook

        runbook["headline"] = "Build detail queue"
        runbook["steps"] = [
            {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/detail_queue_builder.py {td} {orch.get('detailLimit', 5)}"},
            {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/detail_batch_driver.py init {td}"},
            {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/browser_ops_orchestrator.py phase {td} detail"},
        ]
        return runbook

    if phase == "detail-queue":
        runbook["headline"] = "Build detail queue"
        runbook["steps"] = [
            {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/detail_queue_builder.py {td} {orch.get('detailLimit', 5)}"},
            {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/detail_batch_driver.py init {td}"},
            {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/browser_ops_orchestrator.py phase {td} detail"},
        ]
        return runbook

    if phase == "detail":
        idx = batch.get("currentIndex", 0)
        items = batch.get("items", [])
        if idx >= len(items):
            runbook["headline"] = "Finalize report"
            runbook["steps"] = [
                {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/report_builder.py {td}"}
            ]
            return runbook

        item = items[idx]
        target_file = _next_detail_filename(td, idx + 1)
        url = item.get("link", "")
        runbook["headline"] = f"Process detail item {idx + 1}"
        runbook["item"] = item
        runbook["steps"] = [
            {"kind": "browser.open", "url": url, "settleMs": interaction.get("timing", {}).get("pageSettleMs", [1200, 3200])},
            {"kind": "browser.snapshot", "saveTo": target_file, "pauseBeforeMs": interaction.get("timing", {}).get("elementConfirmPauseMs", [300, 900])},
            {
                "kind": "exec",
                "command": f"python3 skills/browser-ops/scripts/browser_detail_processor.py {td} {target_file} '{url}' '{url}'"
            },
            {
                "kind": "exec",
                "command": f"python3 skills/browser-ops/scripts/detail_batch_driver.py done {td}"
            },
            {
                "kind": "exec",
                "command": f"python3 skills/browser-ops/scripts/artifact_recorder.py artifact {td} snapshot {target_file} '{url}' 'detail snapshot'"
            },
        ]
        return runbook

    runbook["headline"] = "Build final report"
    runbook["steps"] = [
        {"kind": "exec", "command": f"python3 skills/browser-ops/scripts/report_builder.py {td}"}
    ]
    return runbook


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: browser_runbook_builder.py <task_dir>", file=sys.stderr)
        raise SystemExit(1)
    rb = build_runbook(sys.argv[1])
    out = Path(sys.argv[1]) / "runbook.json"
    save_json(str(out), rb)
    print(json.dumps({"ok": True, "runbookPath": str(out), "headline": rb.get('headline', '')}, ensure_ascii=False))
