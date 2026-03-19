#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from browser_ops.core.state_store import load_json, save_json


def init_batch(task_dir: str) -> dict:
    td = Path(task_dir)
    queue = load_json(str(td / "detail_queue.json"), default={}).get("items", [])
    state = {
        "status": "ready",
        "queueSize": len(queue),
        "currentIndex": 0,
        "completed": 0,
        "failed": 0,
        "items": queue,
    }
    save_json(str(td / "detail_batch_state.json"), state)
    return state


def next_item(task_dir: str) -> dict:
    td = Path(task_dir)
    state = load_json(str(td / "detail_batch_state.json"), default={})
    idx = state.get("currentIndex", 0)
    items = state.get("items", [])
    if idx >= len(items):
        state["status"] = "completed"
        save_json(str(td / "detail_batch_state.json"), state)
        return {"ok": True, "done": True}
    item = items[idx]
    state["status"] = "running"
    save_json(str(td / "detail_batch_state.json"), state)
    return {"ok": True, "done": False, "index": idx, "item": item}


def mark_done(task_dir: str) -> dict:
    td = Path(task_dir)
    state = load_json(str(td / "detail_batch_state.json"), default={})
    state["currentIndex"] = state.get("currentIndex", 0) + 1
    state["completed"] = state.get("completed", 0) + 1
    if state["currentIndex"] >= len(state.get("items", [])):
        state["status"] = "completed"
    save_json(str(td / "detail_batch_state.json"), state)
    return state


def mark_fail(task_dir: str, reason: str) -> dict:
    td = Path(task_dir)
    state = load_json(str(td / "detail_batch_state.json"), default={})
    idx = state.get("currentIndex", 0)
    item = state.get("items", [])[idx] if idx < len(state.get("items", [])) else {}
    fails = load_json(str(td / "detail_failures.json"), default=[])
    fails.append({"index": idx, "item": item, "reason": reason})
    save_json(str(td / "detail_failures.json"), fails)
    state["currentIndex"] = idx + 1
    state["failed"] = state.get("failed", 0) + 1
    if state["currentIndex"] >= len(state.get("items", [])):
        state["status"] = "completed"
    save_json(str(td / "detail_batch_state.json"), state)
    return state


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("Usage: detail_batch_driver.py <init|next|done|fail> <task_dir> [reason]", file=sys.stderr)
        return 1
    cmd = argv[1]
    task_dir = argv[2]
    if cmd == "init":
        print(json.dumps(init_batch(task_dir), ensure_ascii=False))
        return 0
    if cmd == "next":
        print(json.dumps(next_item(task_dir), ensure_ascii=False))
        return 0
    if cmd == "done":
        print(json.dumps(mark_done(task_dir), ensure_ascii=False))
        return 0
    if cmd == "fail":
        reason = argv[3] if len(argv) > 3 else "unknown"
        print(json.dumps(mark_fail(task_dir, reason), ensure_ascii=False))
        return 0
    raise SystemExit(f"unknown command: {cmd}")
