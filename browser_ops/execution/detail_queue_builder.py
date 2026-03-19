#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from browser_ops.core.state_store import save_json


def build_queue(task_dir: str, limit: int = 10) -> dict:
    td = Path(task_dir)
    results = td / "results.jsonl"
    done = set()
    detail_results = td / "detail_results.jsonl"
    if detail_results.exists():
        for line in detail_results.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if obj.get("sourceItemLink"):
                    done.add(obj["sourceItemLink"])
                elif obj.get("url"):
                    done.add(obj["url"])
            except Exception:
                pass

    queue = []
    if results.exists():
        for line in results.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("kind") == "pagination":
                continue
            link = obj.get("link")
            if not link or link in done:
                continue
            queue.append({
                "title": obj.get("title", ""),
                "link": link,
                "source": obj.get("source", ""),
            })
            if len(queue) >= limit:
                break

    out = {"queueSize": len(queue), "items": queue}
    save_json(str(td / "detail_queue.json"), out)
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: detail_queue_builder.py <task_dir> [limit]", file=sys.stderr)
        return 1
    limit = int(argv[2]) if len(argv) > 2 else 10
    print(json.dumps(build_queue(argv[1], limit), ensure_ascii=False))
    return 0
