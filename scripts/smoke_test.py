#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TASK_DIR = Path('/tmp/browser_ops_smoke_test')
PROFILE = ROOT / 'assets' / 'example_profiles' / 'hackernews-browser.json'

def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stdout)
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(proc.returncode)

def assert_exists(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f'missing expected file: {path}')

def main() -> int:
    if TASK_DIR.exists():
        shutil.rmtree(TASK_DIR)
    TASK_DIR.mkdir(parents=True, exist_ok=True)

    run([sys.executable, str(ROOT / 'scripts' / 'device_profile_manager.py'), str(TASK_DIR), 'mobile-default'])
    run([sys.executable, str(ROOT / 'scripts' / 'browser_human_mode.py'), 'enable', str(TASK_DIR), 'human-assisted', 'balanced'])
    run([sys.executable, str(ROOT / 'scripts' / 'action_policy_engine.py'), str(TASK_DIR), str(PROFILE)])
    run([sys.executable, str(ROOT / 'scripts' / 'browser_ops_orchestrator.py'), 'init', str(PROFILE), str(TASK_DIR), '3', '2', 'false'])
    run([sys.executable, str(ROOT / 'scripts' / 'browser_plan_builder.py'), str(PROFILE), str(TASK_DIR)])
    run([sys.executable, str(ROOT / 'scripts' / 'browser_runbook_builder.py'), str(TASK_DIR)])
    run([sys.executable, str(ROOT / 'scripts' / 'browser_handoff_payload.py'), str(TASK_DIR)])
    run([sys.executable, str(ROOT / 'scripts' / 'site_connectivity_adapter.py'), 'https://news.ycombinator.com/news', str(PROFILE), str(TASK_DIR)])
    run([sys.executable, str(ROOT / 'scripts' / 'autopilot_tick.py'), str(TASK_DIR)])
    run([sys.executable, str(ROOT / 'scripts' / 'failure_recovery_engine.py'), 'plan', str(TASK_DIR)])
    run([sys.executable, str(ROOT / 'scripts' / 'recovery_runbook_builder.py'), str(TASK_DIR)])

    for rel in [
        'action_policy.json',
        'browser_plan.json',
        'runbook.json',
        'browser_handoff_payload.json',
        'connectivity_report.json',
        'runbook.exec.json',
        'recovery_plan.json',
        'recovery_runbook.json',
    ]:
        assert_exists(TASK_DIR / rel)

    report = {
        'ok': True,
        'taskDir': str(TASK_DIR),
        'checkedFiles': [
            'action_policy.json',
            'browser_plan.json',
            'runbook.json',
            'browser_handoff_payload.json',
            'runbook.exec.json',
            'recovery_plan.json',
            'recovery_runbook.json',
        ]
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print('\n✅ smoke test passed')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
