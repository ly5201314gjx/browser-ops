#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def _register_failure(base: Path, td: Path, stage: str, reason: str) -> None:
    run([
        sys.executable,
        str(base / 'failure_recovery_engine.py'),
        'register',
        str(td),
        stage,
        reason,
        '', '', '', 'true'
    ])


def tick(task_dir: str) -> dict:
    td = Path(task_dir).resolve()
    base = Path(__file__).resolve().parent

    rb = run([sys.executable, str(base / 'browser_runbook_builder.py'), str(td)])
    if rb.returncode != 0:
        _register_failure(base, td, 'build_runbook', 'browser_runbook_builder failed')
        return {"ok": False, "stage": "build_runbook", "stderr": rb.stderr, "stdout": rb.stdout}

    handoff = run([sys.executable, str(base / 'browser_handoff_payload.py'), str(td)])
    if handoff.returncode != 0:
        _register_failure(base, td, 'build_handoff_payload', 'browser_handoff_payload failed')
        return {"ok": False, "stage": "build_handoff_payload", "stderr": handoff.stderr, "stdout": handoff.stdout}

    runbook_path = td / 'runbook.json'
    ex = run([sys.executable, str(base / 'runbook_executor.py'), str(runbook_path), '/home/lg030452/.openclaw/workspace'])
    if ex.returncode != 0:
        _register_failure(base, td, 'execute_runbook', 'runbook_executor crashed')
        return {"ok": False, "stage": "execute_runbook", "stderr": ex.stderr, "stdout": ex.stdout}

    report = json.loads(ex.stdout)
    handoff_report = json.loads(handoff.stdout)
    if report.get('failed'):
        reason = f"runbook execution failed in phase={report.get('phase', '')} headline={report.get('headline', '')}"
        _register_failure(base, td, 'execute_runbook', reason)

    return {
        "ok": True,
        "taskDir": str(td),
        "runbookPath": str(runbook_path),
        "browserHandoffPayload": handoff_report,
        "exec": report,
    }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: autopilot_tick.py <task_dir>', file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(tick(sys.argv[1]), ensure_ascii=False, indent=2))
