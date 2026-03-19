#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def main(task_dir: str) -> int:
    td = Path(task_dir).resolve()
    td.mkdir(parents=True, exist_ok=True)
    base = Path(__file__).resolve().parent
    profile = base.parent / "assets" / "example_profiles" / "hackernews-browser.json"

    cmds = [
        [sys.executable, str(base / "browser_ops_orchestrator.py"), "init", str(profile), str(td), "3", "2"],
        [sys.executable, str(base / "browser_runbook_builder.py"), str(td)],
    ]

    outputs = []
    for cmd in cmds:
        proc = subprocess.run(cmd, capture_output=True, text=True)
        outputs.append({
            "cmd": cmd,
            "code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
        })
        if proc.returncode != 0:
            print(json.dumps({"ok": False, "outputs": outputs}, ensure_ascii=False, indent=2))
            return proc.returncode

    guide = {
        "taskDir": str(td),
        "nextFiles": {
            "orchestrator": str(td / "orchestrator_state.json"),
            "runbook": str(td / "runbook.json"),
        },
        "howToUse": [
            "1. Read runbook.json",
            "2. Use OpenClaw browser.open on the runbook URL",
            "3. Use browser.snapshot and save to the advised file",
            "4. Run the advised script commands",
            "5. Regenerate runbook as the workflow advances"
        ]
    }
    (td / "demo_guide.json").write_text(json.dumps(guide, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "taskDir": str(td), "guide": guide}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: hn_demo_setup.py <task_dir>", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1]))
