#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from browser_ops.core.profile_runner import load_profile
from browser_ops.core.state_store import load_json, save_json
from browser_ops.policy.interaction_policy_engine import DEFAULT_POLICIES


def build_action_policy(task_dir: str, profile_path: str | None = None) -> dict:
    td = Path(task_dir)
    profile = load_profile(profile_path) if profile_path else load_json(str(td / "resolved_profile.json"), default={})
    device_profile = load_json(str(td / "device_profile.json"), default={})
    human_mode = load_json(str(td / "human_mode.json"), default={})
    existing_interaction = load_json(str(td / "interaction_policy.json"), default={})
    deep = load_json(str(td / "deep_analysis.json"), default={})

    preferred_device = profile.get("preferredDevice") or device_profile.get("name") or existing_interaction.get("device") or "mobile-default"
    base_policy = json.loads(json.dumps(DEFAULT_POLICIES.get(preferred_device, DEFAULT_POLICIES["mobile-default"])))

    profile_policy = profile.get("interactionPolicy", {})
    checkpoint_policy = profile.get("checkpointPolicy", {})
    navigation_style = profile.get("navigationStyle", "stepwise-visible")
    risk_tolerance = profile.get("riskTolerance", "balanced")

    action_policy = {
        "device": preferred_device,
        "navigationStyle": navigation_style,
        "riskTolerance": risk_tolerance,
        "checkpointPolicy": {
            "pauseOnLogin": checkpoint_policy.get("pauseOnLogin", True),
            "pauseOnMfa": checkpoint_policy.get("pauseOnMfa", True),
            "pauseOnCaptcha": checkpoint_policy.get("pauseOnCaptcha", True),
            "pauseOnApproval": checkpoint_policy.get("pauseOnApproval", True),
        },
        "interactionPolicy": base_policy,
        "profileOverrides": profile_policy,
        "humanMode": human_mode,
    }

    for section, values in profile_policy.items():
        if isinstance(values, dict) and isinstance(action_policy["interactionPolicy"].get(section), dict):
            action_policy["interactionPolicy"][section].update(values)

    automation_difficulty = deep.get("summary", {}).get("automationDifficulty", 0)
    human_needed = deep.get("finalJudgement", {}).get("humanCheckpointNeeded", False)
    complexity = deep.get("dimensions", {}).get("interaction_complexity", {}).get("complexityScore", 0)

    if automation_difficulty >= 4 or human_needed:
        action_policy["riskTolerance"] = "conservative"
        action_policy["checkpointPolicy"].update({
            "pauseOnLogin": True,
            "pauseOnMfa": True,
            "pauseOnCaptcha": True,
            "pauseOnApproval": True,
        })
        action_policy["interactionPolicy"].get("timing", {}).update({
            "pageSettleMs": [1400, 3600],
            "betweenActionsMs": [250, 900],
        })
    elif complexity >= 4:
        action_policy["interactionPolicy"].get("timing", {}).update({
            "pageSettleMs": [1300, 3200],
            "betweenActionsMs": [220, 800],
        })

    action_policy["deepAnalysisSummary"] = {
        "automationDifficulty": automation_difficulty,
        "humanCheckpointNeeded": human_needed,
        "interactionComplexity": complexity,
    }

    save_json(str(td / "action_policy.json"), action_policy)
    if profile_path:
        save_json(str(td / "resolved_profile.json"), profile)
    return action_policy


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3):
        print("Usage: action_policy_engine.py <task_dir> [profile.json]", file=sys.stderr)
        return 1
    result = build_action_policy(argv[1], argv[2] if len(argv) == 3 else None)
    print(json.dumps({"ok": True, "output": str(Path(argv[1]) / 'action_policy.json'), "device": result['device']}, ensure_ascii=False))
    return 0
