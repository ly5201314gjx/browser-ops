#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from state_store import save_json


def execute_runbook(runbook_path: str, cwd: str | None = None) -> dict:
    rb_path = Path(runbook_path).resolve()
    runbook = json.loads(rb_path.read_text(encoding="utf-8"))
    base_cwd = Path(cwd).resolve() if cwd else Path('/home/lg030452/.openclaw/workspace').resolve()

    results = []
    pending_browser = []
    blocked_after_browser = []
    failed = False
    browser_boundary_hit = False

    for idx, step in enumerate(runbook.get("steps", []), start=1):
        kind = step.get("kind", "")
        if kind.startswith("browser."):
            browser_boundary_hit = True
            pending_browser.append({"index": idx, **step})
            continue

        if browser_boundary_hit:
            blocked_after_browser.append({"index": idx, **step})
            continue

        if kind == "note":
            results.append({"index": idx, "kind": kind, "status": "noted", "text": step.get("text", "")})
            continue

        if kind == "exec":
            cmd = step.get("command", "")
            proc = subprocess.run(cmd, shell=True, cwd=str(base_cwd), capture_output=True, text=True)
            item = {
                "index": idx,
                "kind": kind,
                "command": cmd,
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
            }
            if proc.returncode == 0:
                item["status"] = "done"
            else:
                item["status"] = "failed"
                failed = True
                results.append(item)
                break
            results.append(item)
            continue

        results.append({"index": idx, "kind": kind, "status": "skipped-unknown"})

    action_policy = runbook.get("actionPolicy", {})
    summary = {
        "ok": (not failed),
        "runbookPath": str(rb_path),
        "phase": runbook.get("phase", ""),
        "headline": runbook.get("headline", ""),
        "effectiveRoute": runbook.get("effectiveRoute", "browser"),
        "actionPolicySummary": {
            "device": action_policy.get("device"),
            "navigationStyle": action_policy.get("navigationStyle"),
            "riskTolerance": action_policy.get("riskTolerance"),
            "checkpointPolicy": action_policy.get("checkpointPolicy", {}),
        },
        "results": results,
        "pendingBrowserSteps": pending_browser,
        "pendingBrowserStepCount": len(pending_browser),
        "blockedAfterBrowser": blocked_after_browser,
        "blockedAfterBrowserCount": len(blocked_after_browser),
        "stoppedAtBrowserBoundary": browser_boundary_hit,
        "failed": failed,
    }
    out = rb_path.with_suffix('.exec.json')
    save_json(str(out), summary)
    return summary


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: runbook_executor.py <runbook.json> [cwd]', file=sys.stderr)
        raise SystemExit(1)
    cwd = sys.argv[2] if len(sys.argv) > 2 else None
    result = execute_runbook(sys.argv[1], cwd)
    print(json.dumps({
        'ok': result['ok'],
        'execReport': str(Path(sys.argv[1]).with_suffix('.exec.json')),
        'pendingBrowserSteps': len(result['pendingBrowserSteps']),
        'blockedAfterBrowser': result['blockedAfterBrowserCount'],
        'failed': result['failed'],
        'device': result['actionPolicySummary'].get('device'),
        'stoppedAtBrowserBoundary': result['stoppedAtBrowserBoundary'],
    }, ensure_ascii=False))
