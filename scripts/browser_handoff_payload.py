#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from state_store import load_json, save_json


def build_payload(task_dir: str) -> dict:
    td = Path(task_dir)
    runbook = load_json(str(td / "runbook.json"), default={})
    action_policy = load_json(str(td / "action_policy.json"), default={})
    pending = []
    for idx, step in enumerate(runbook.get("steps", []), start=1):
        kind = step.get("kind", "")
        if kind.startswith("browser."):
            pending.append({"index": idx, **step})

    payload = {
        "taskDir": str(td),
        "phase": runbook.get("phase", ""),
        "headline": runbook.get("headline", ""),
        "effectiveRoute": runbook.get("effectiveRoute", "browser"),
        "actionPolicy": {
            "device": action_policy.get("device"),
            "navigationStyle": action_policy.get("navigationStyle"),
            "riskTolerance": action_policy.get("riskTolerance"),
            "checkpointPolicy": action_policy.get("checkpointPolicy", {}),
            "interactionPolicy": action_policy.get("interactionPolicy", {}),
        },
        "browserSteps": pending,
    }
    save_json(str(td / "browser_handoff_payload.json"), payload)
    return payload


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: browser_handoff_payload.py <task_dir>", file=sys.stderr)
        raise SystemExit(1)
    result = build_payload(sys.argv[1])
    print(json.dumps({"ok": True, "output": str(Path(sys.argv[1]) / 'browser_handoff_payload.json'), "browserSteps": len(result['browserSteps'])}, ensure_ascii=False))
