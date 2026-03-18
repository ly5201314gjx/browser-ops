#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from state_store import load_json, save_json


def build_packet(task_dir: str, reason: str, current_url: str = "", screenshot_path: str = "", snapshot_path: str = "") -> dict:
    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    device = load_json(str(td / "device_profile.json"), default={})
    action_policy = load_json(str(td / "action_policy.json"), default={})
    browser_payload = load_json(str(td / "browser_handoff_payload.json"), default={})
    packet = {
        "createdAt": datetime.now().isoformat(),
        "reason": reason,
        "currentUrl": current_url or runtime.get("lastUrl", "") or orch.get("startUrl", ""),
        "screenshotPath": screenshot_path,
        "snapshotPath": snapshot_path,
        "phase": orch.get("currentPhase", ""),
        "effectiveRoute": orch.get("intelligence", {}).get("recommendedRoute") or orch.get("route", "browser"),
        "deviceProfile": device,
        "actionPolicy": {
            "device": action_policy.get("device"),
            "navigationStyle": action_policy.get("navigationStyle"),
            "riskTolerance": action_policy.get("riskTolerance"),
            "checkpointPolicy": action_policy.get("checkpointPolicy", {}),
            "interactionPolicy": action_policy.get("interactionPolicy", {}),
        },
        "browserHandoffPayload": browser_payload,
        "instructionsForHuman": [
            "Complete the blocked step in the browser (e.g. login, MFA, approval, or navigation checkpoint).",
            "Follow the provided action policy and browser step context when practical.",
            "Do not change unrelated page state if avoidable.",
            "After handoff is complete, resume the workflow from this task directory."
        ]
    }
    save_json(str(td / "handoff_packet.json"), packet)
    return packet


def mark_resume(task_dir: str, note: str = "human handoff completed") -> dict:
    td = Path(task_dir)
    packet = load_json(str(td / "handoff_packet.json"), default={})
    packet["resumedAt"] = datetime.now().isoformat()
    packet["resumeNote"] = note
    save_json(str(td / "handoff_packet.json"), packet)
    return packet


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: handoff_packet.py <build|resume> <task_dir> [args...]", file=sys.stderr)
        raise SystemExit(1)
    cmd = sys.argv[1]
    if cmd == "build":
        reason = sys.argv[3] if len(sys.argv) > 3 else "human-checkpoint"
        current_url = sys.argv[4] if len(sys.argv) > 4 else ""
        screenshot = sys.argv[5] if len(sys.argv) > 5 else ""
        snapshot = sys.argv[6] if len(sys.argv) > 6 else ""
        print(json.dumps(build_packet(sys.argv[2], reason, current_url, screenshot, snapshot), ensure_ascii=False, indent=2))
    elif cmd == "resume":
        note = sys.argv[3] if len(sys.argv) > 3 else "human handoff completed"
        print(json.dumps(mark_resume(sys.argv[2], note), ensure_ascii=False, indent=2))
    else:
        raise SystemExit(f"unknown command: {cmd}")
