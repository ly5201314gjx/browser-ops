#!/usr/bin/env python3
"""
Run a browser-ops job from a JSON config.
MVP version: route selection, task folder setup, state/log/output scaffolding.
Browser interaction is orchestrated by OpenClaw browser tool from the main agent; this script
focuses on deterministic task structure, state, and outputs.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

from state_store import save_json


def main(config_path: str):
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    task_name = cfg.get("taskName", "browser-job")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_dir = Path(cfg.get("taskDir", f"logs/browser-ops/{task_name}_{ts}"))
    task_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "taskName": task_name,
        "createdAt": datetime.now().isoformat(),
        "route": cfg.get("route", "browser"),
        "status": "initialized",
        "pagesVisited": 0,
        "itemsExtracted": 0,
        "failedUrls": [],
        "configPath": str(Path(config_path).resolve()),
    }
    save_json(str(task_dir / "state.json"), state)
    save_json(str(task_dir / "job.json"), cfg)
    (task_dir / "run.log").write_text("initialized\n", encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "taskDir": str(task_dir),
        "route": state["route"],
        "message": "Task initialized. Use browser tool or orchestrator to execute steps."
    }, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: run_browser_job.py <job.json>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
