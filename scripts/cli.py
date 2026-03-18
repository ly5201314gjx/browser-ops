#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

COMMAND_MAP = {
    "doctor": [sys.executable, str(SCRIPTS / "doctor.py")],
    "smoke-test": [sys.executable, str(SCRIPTS / "smoke_test.py")],
    "demo": [str(ROOT / "demo.sh")],
    "install": [str(ROOT / "install.sh")],
    "init": [sys.executable, str(SCRIPTS / "browser_ops_orchestrator.py"), "init"],
    "status": [sys.executable, str(SCRIPTS / "browser_ops_orchestrator.py"), "status"],
    "next": [sys.executable, str(SCRIPTS / "browser_ops_orchestrator.py"), "next"],
    "runbook": [sys.executable, str(SCRIPTS / "browser_runbook_builder.py")],
    "handoff": [sys.executable, str(SCRIPTS / "browser_handoff_payload.py")],
    "recover-plan": [sys.executable, str(SCRIPTS / "failure_recovery_engine.py"), "plan"],
    "recover-runbook": [sys.executable, str(SCRIPTS / "recovery_runbook_builder.py")],
}

HELP = """Browser Ops CLI

Usage:
  browser-ops doctor
  browser-ops smoke-test
  browser-ops demo
  browser-ops install
  browser-ops init <profile.json> <task_dir> [detail_limit] [page_limit] [intelligence_first]
  browser-ops status <task_dir>
  browser-ops next <task_dir>
  browser-ops runbook <task_dir>
  browser-ops handoff <task_dir>
  browser-ops recover-plan <task_dir>
  browser-ops recover-runbook <task_dir>
"""


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"}:
        print(HELP)
        return 0
    cmd = sys.argv[1]
    args = sys.argv[2:]
    base = COMMAND_MAP.get(cmd)
    if not base:
        print(f"unknown command: {cmd}", file=sys.stderr)
        print(HELP, file=sys.stderr)
        return 1
    proc = subprocess.run(base + args, cwd=str(ROOT))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
