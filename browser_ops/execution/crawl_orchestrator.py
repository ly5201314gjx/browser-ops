#!/usr/bin/env python3
"""Profile-driven crawl orchestrator."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

from browser_ops.core.profile_runner import load_profile
from browser_ops.core.state_store import save_json


def initialize(profile: dict, out_dir: str | None = None) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_dir = Path(out_dir or f"logs/browser-ops/{profile['name']}_{ts}")
    task_dir.mkdir(parents=True, exist_ok=True)

    state = {
        "profile": profile["name"],
        "route": profile.get("route", "browser"),
        "createdAt": datetime.now().isoformat(),
        "status": "initialized",
        "pagesVisited": 0,
        "itemsExtracted": 0,
        "failedUrls": [],
        "queue": profile.get("startUrls", []),
        "visited": [],
    }

    save_json(str(task_dir / "profile.json"), profile)
    save_json(str(task_dir / "state.json"), state)
    (task_dir / "results.jsonl").touch()
    (task_dir / "failed_urls.json").write_text("[]", encoding="utf-8")
    (task_dir / "run.log").write_text("crawl initialized\n", encoding="utf-8")
    return task_dir


def main(profile_path: str, out_dir: str | None = None):
    profile = load_profile(profile_path)
    task_dir = initialize(profile, out_dir)
    route = profile.get("route", "browser")

    if route == "http":
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "http_crawler.py"), profile_path, str(task_dir), "list"],
            capture_output=True,
            text=True,
        )
        print(proc.stdout.strip() or proc.stderr.strip())
        return

    if route in {"browser", "hybrid", "human"}:
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent.parent.parent / "scripts" / "browser_plan_builder.py"), profile_path, str(task_dir)],
            capture_output=True,
            text=True,
        )
        print(proc.stdout.strip() or proc.stderr.strip())
        return

    raise SystemExit(f"unsupported route: {route}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: crawl_orchestrator.py <profile.json> [out_dir]", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
