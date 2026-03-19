#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from browser_ops.core.state_store import save_json
from browser_ops.recovery.failure_recovery_engine import build_recovery_plan


def build_runbook(task_dir: str) -> dict:
    td = Path(task_dir)
    plan = build_recovery_plan(task_dir)
    steps = []
    for action in plan.get("recommendedActions", []):
        kind = action.get("kind")
        if kind == "auto-resolve-incident":
            steps.append({"kind": "note", "text": action.get("reason", "")})
            steps.append({"kind": "exec", "command": f"python3 skills/browser-ops/scripts/failure_recovery_engine.py resolve {td} {action.get('incidentId')} 'auto-resolved by recovery hook'"})
        elif kind == "resume-browser-slice":
            steps.append({"kind": "note", "text": action.get("reason", "")})
            steps.append({"kind": "exec", "command": f"python3 skills/browser-ops/scripts/browser_handoff_payload.py {td}"})
        elif kind == "retry-last-failed-slice":
            steps.append({"kind": "note", "text": action.get("reason", "")})
            steps.append({"kind": "exec", "command": f"python3 skills/browser-ops/scripts/failure_recovery_engine.py bump-retry {td} {action.get('incidentId')}"})
            steps.append({"kind": "exec", "command": f"python3 skills/browser-ops/scripts/autopilot_tick.py {td}"})
        elif kind == "human-review":
            steps.append({"kind": "note", "text": action.get("reason", "")})
            steps.append({"kind": "exec", "command": f"python3 skills/browser-ops/scripts/handoff_packet.py build {td} recovery-review '' '' ''"})
        elif kind == "resume-detail-index":
            steps.append({"kind": "note", "text": action.get("reason", "")})
        elif kind == "resume-list-phase":
            steps.append({"kind": "note", "text": action.get("reason", "")})
        elif kind == "rebuild-report":
            steps.append({"kind": "exec", "command": f"python3 skills/browser-ops/scripts/report_builder.py {td}"})

    runbook = {
        "taskDir": str(td),
        "phase": plan.get("phase", ""),
        "headline": "Recovery runbook",
        "openIncidents": len(plan.get("openIncidents", [])),
        "deepAnalysisSummary": plan.get("deepAnalysisSummary", {}),
        "recommendedActions": plan.get("recommendedActions", []),
        "steps": steps,
    }
    save_json(str(td / "recovery_runbook.json"), runbook)
    return runbook


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: recovery_runbook_builder.py <task_dir>", file=sys.stderr)
        return 1
    rb = build_runbook(argv[1])
    print(json.dumps({"ok": True, "output": str(Path(argv[1]) / 'recovery_runbook.json'), "steps": len(rb['steps'])}, ensure_ascii=False))
    return 0
