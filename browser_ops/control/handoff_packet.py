#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime

from browser_ops.core.state_store import load_json, save_json


def build_packet(task_dir: str, reason: str, current_url: str = "", screenshot_path: str = "", snapshot_path: str = "") -> dict:
    from pathlib import Path

    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    device = load_json(str(td / "device_profile.json"), default={})
    action_policy = load_json(str(td / "action_policy.json"), default={})
    browser_payload = load_json(str(td / "browser_handoff_payload.json"), default={})
    deep = load_json(str(td / "deep_analysis.json"), default={})
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
        "deepAnalysisSummary": {
            "siteType": deep.get("summary", {}).get("siteType"),
            "recommendedRoute": deep.get("summary", {}).get("recommendedRoute"),
            "automationDifficulty": deep.get("summary", {}).get("automationDifficulty"),
            "extractionValue": deep.get("summary", {}).get("extractionValue"),
            "humanCheckpointNeeded": deep.get("finalJudgement", {}).get("humanCheckpointNeeded"),
            "bestResearchMode": deep.get("finalJudgement", {}).get("bestResearchMode"),
        },
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
    from pathlib import Path

    td = Path(task_dir)
    packet = load_json(str(td / "handoff_packet.json"), default={})
    packet["resumedAt"] = datetime.now().isoformat()
    packet["resumeNote"] = note
    save_json(str(td / "handoff_packet.json"), packet)
    return packet


def main(argv: list[str]) -> int:
    import sys

    if len(argv) < 3:
        print("Usage: handoff_packet.py <build|resume> <task_dir> [args...]", file=sys.stderr)
        return 1
    cmd = argv[1]
    if cmd == "build":
        reason = argv[3] if len(argv) > 3 else "human-checkpoint"
        current_url = argv[4] if len(argv) > 4 else ""
        screenshot = argv[5] if len(argv) > 5 else ""
        snapshot = argv[6] if len(argv) > 6 else ""
        print(json.dumps(build_packet(argv[2], reason, current_url, screenshot, snapshot), ensure_ascii=False, indent=2))
        return 0
    if cmd == "resume":
        note = argv[3] if len(argv) > 3 else "human handoff completed"
        print(json.dumps(mark_resume(argv[2], note), ensure_ascii=False, indent=2))
        return 0
    raise SystemExit(f"unknown command: {cmd}")
