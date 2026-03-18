#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from state_store import load_json


def advise(task_dir: str) -> dict:
    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    batch = load_json(str(td / "detail_batch_state.json"), default={})

    phase = orch.get("currentPhase", "list")
    if phase == "list":
        visited = runtime.get("pagesVisited", 0)
        next_url = runtime.get("suggestedNextUrl", "")
        if visited == 0:
            return {
                "phase": "list",
                "headline": "Open the start URL and process page 1",
                "commands": [
                    "browser.open <start_url>",
                    "browser.snapshot",
                    "save snapshot to page1.txt",
                    "browser_page_processor.py <task_dir> page1.txt <start_url>"
                ]
            }
        if next_url:
            return {
                "phase": "list",
                "headline": "Continue pagination",
                "commands": [
                    f"browser.navigate {next_url}",
                    "browser.snapshot",
                    "save snapshot to next page file",
                    f"browser_page_processor.py <task_dir> <pageN.txt> {next_url}"
                ]
            }
        return {
            "phase": "list",
            "headline": "List phase done; build detail queue",
            "commands": [
                "detail_queue_builder.py <task_dir> <limit>",
                "detail_batch_driver.py init <task_dir>",
                "browser_ops_orchestrator.py phase <task_dir> detail"
            ]
        }

    if phase == "detail":
        idx = batch.get("currentIndex", 0)
        items = batch.get("items", [])
        if idx >= len(items):
            return {
                "phase": "detail",
                "headline": "Detail phase complete; build report",
                "commands": ["report_builder.py <task_dir>"]
            }
        item = items[idx]
        return {
            "phase": "detail",
            "headline": f"Open detail item #{idx+1}",
            "commands": [
                f"browser.open {item.get('link', '')}",
                "browser.snapshot",
                "save snapshot to detail-N.txt",
                f"browser_detail_processor.py <task_dir> <detail-N.txt> {item.get('link', '')} {item.get('link', '')}",
                "detail_batch_driver.py done <task_dir>"
            ],
            "item": item,
        }

    return {
        "phase": phase,
        "headline": "Build final report",
        "commands": ["report_builder.py <task_dir>"]
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: browser_next_step.py <task_dir>", file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(advise(sys.argv[1]), ensure_ascii=False, indent=2))
