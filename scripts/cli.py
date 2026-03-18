#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"

HELP = """Browser Ops CLI

Usage:
  browser-ops doctor
  browser-ops smoke-test
  browser-ops demo [--profile <profile.json>] [--task-dir <dir>]
  browser-ops install
  browser-ops init <profile.json> <task_dir> [detail_limit] [page_limit] [intelligence_first]
  browser-ops status <task_dir>
  browser-ops next <task_dir>
  browser-ops runbook <task_dir>
  browser-ops handoff <task_dir>
  browser-ops recover-plan <task_dir>
  browser-ops recover-runbook <task_dir>
"""


def run(cmd: list[str]) -> int:
    proc = subprocess.run(cmd, cwd=str(ROOT))
    return proc.returncode


def parse_flag(args: list[str], name: str, default: str) -> str:
    if name in args:
        idx = args.index(name)
        if idx + 1 < len(args):
            return args[idx + 1]
    return default


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help", "help"}:
        print(HELP)
        return 0

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "doctor":
        return run([sys.executable, str(SCRIPTS / "doctor.py")])
    if cmd == "smoke-test":
        return run([sys.executable, str(SCRIPTS / "smoke_test.py")])
    if cmd == "install":
        return run([str(ROOT / "install.sh")])
    if cmd == "demo":
        profile = parse_flag(args, "--profile", str(ROOT / "assets" / "example_profiles" / "hackernews-browser.json"))
        task_dir = parse_flag(args, "--task-dir", "/tmp/browser_ops_demo_release")
        return run([str(ROOT / "demo.sh"), profile, task_dir])
    if cmd == "init":
        return run([sys.executable, str(SCRIPTS / "browser_ops_orchestrator.py"), "init", *args])
    if cmd == "status":
        return run([sys.executable, str(SCRIPTS / "browser_ops_orchestrator.py"), "status", *args])
    if cmd == "next":
        return run([sys.executable, str(SCRIPTS / "browser_ops_orchestrator.py"), "next", *args])
    if cmd == "runbook":
        return run([sys.executable, str(SCRIPTS / "browser_runbook_builder.py"), *args])
    if cmd == "handoff":
        return run([sys.executable, str(SCRIPTS / "browser_handoff_payload.py"), *args])
    if cmd == "recover-plan":
        return run([sys.executable, str(SCRIPTS / "failure_recovery_engine.py"), "plan", *args])
    if cmd == "recover-runbook":
        return run([sys.executable, str(SCRIPTS / "recovery_runbook_builder.py"), *args])

    print(f"unknown command: {cmd}", file=sys.stderr)
    print(HELP, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
