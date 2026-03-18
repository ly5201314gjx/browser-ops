#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime

from state_store import append_jsonl, load_json, save_json


def load_plan(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def init_runtime(plan_path: str, task_dir: str) -> dict:
    plan = load_plan(plan_path)
    td = Path(task_dir)
    td.mkdir(parents=True, exist_ok=True)
    runtime = {
        "createdAt": datetime.now().isoformat(),
        "planPath": str(Path(plan_path).resolve()),
        "taskDir": str(td.resolve()),
        "profile": plan.get("profile"),
        "route": plan.get("route", "browser"),
        "currentStep": 0,
        "pagesVisited": 0,
        "itemsExtracted": 0,
        "visitedUrls": [],
        "failedUrls": [],
        "status": "ready",
    }
    save_json(str(td / "browser_runtime.json"), runtime)
    return runtime


def record_page(task_dir: str, url: str, extracted_items: list[dict] | None = None, note: str = "") -> dict:
    td = Path(task_dir)
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    runtime.setdefault("visitedUrls", [])
    runtime.setdefault("failedUrls", [])
    runtime["status"] = "running"
    runtime["lastUrl"] = url
    if url not in runtime["visitedUrls"]:
        runtime["visitedUrls"].append(url)
        runtime["pagesVisited"] = runtime.get("pagesVisited", 0) + 1

    extracted_items = extracted_items or []
    for item in extracted_items:
        append_jsonl(str(td / "results.jsonl"), item)
    runtime["itemsExtracted"] = runtime.get("itemsExtracted", 0) + len(extracted_items)
    if note:
        runtime["lastNote"] = note
    save_json(str(td / "browser_runtime.json"), runtime)
    return runtime


def record_failure(task_dir: str, url: str, reason: str) -> dict:
    td = Path(task_dir)
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    runtime.setdefault("failedUrls", []).append({"url": url, "reason": reason})
    runtime["status"] = "failed-step"
    save_json(str(td / "browser_runtime.json"), runtime)
    return runtime


def complete(task_dir: str) -> dict:
    td = Path(task_dir)
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    runtime["status"] = "completed"
    runtime["completedAt"] = datetime.now().isoformat()
    save_json(str(td / "browser_runtime.json"), runtime)
    return runtime


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: browser_state_driver.py <init|record|fail|complete> ...", file=sys.stderr)
        return 1
    cmd = argv[1]
    if cmd == "init":
        if len(argv) != 4:
            print("Usage: browser_state_driver.py init <plan.json> <task_dir>", file=sys.stderr)
            return 1
        print(json.dumps(init_runtime(argv[2], argv[3]), ensure_ascii=False))
        return 0
    if cmd == "record":
        if len(argv) < 4:
            print("Usage: browser_state_driver.py record <task_dir> <url> [items_json_path] [note]", file=sys.stderr)
            return 1
        items = []
        if len(argv) >= 5 and argv[4] and Path(argv[4]).exists():
            items = json.loads(Path(argv[4]).read_text(encoding="utf-8"))
        note = argv[5] if len(argv) >= 6 else ""
        print(json.dumps(record_page(argv[2], argv[3], items, note), ensure_ascii=False))
        return 0
    if cmd == "fail":
        if len(argv) != 5:
            print("Usage: browser_state_driver.py fail <task_dir> <url> <reason>", file=sys.stderr)
            return 1
        print(json.dumps(record_failure(argv[2], argv[3], argv[4]), ensure_ascii=False))
        return 0
    if cmd == "complete":
        if len(argv) != 3:
            print("Usage: browser_state_driver.py complete <task_dir>", file=sys.stderr)
            return 1
        print(json.dumps(complete(argv[2]), ensure_ascii=False))
        return 0
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
