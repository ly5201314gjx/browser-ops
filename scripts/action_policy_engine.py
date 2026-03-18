#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from profile_runner import load_profile
from state_store import load_json, save_json
from interaction_policy_engine import DEFAULT_POLICIES


def build_action_policy(task_dir: str, profile_path: str | None = None) -> dict:
    td = Path(task_dir)
    profile = load_profile(profile_path) if profile_path else load_json(str(td / "resolved_profile.json"), default={})
    device_profile = load_json(str(td / "device_profile.json"), default={})
    human_mode = load_json(str(td / "human_mode.json"), default={})
    existing_interaction = load_json(str(td / "interaction_policy.json"), default={})

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

    save_json(str(td / "action_policy.json"), action_policy)
    if profile_path:
        save_json(str(td / "resolved_profile.json"), profile)
    return action_policy


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: action_policy_engine.py <task_dir> [profile.json]", file=sys.stderr)
        raise SystemExit(1)
    result = build_action_policy(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
    print(json.dumps({"ok": True, "output": str(Path(sys.argv[1]) / 'action_policy.json'), "device": result['device']}, ensure_ascii=False))
