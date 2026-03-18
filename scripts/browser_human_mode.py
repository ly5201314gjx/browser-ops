#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from state_store import load_json, save_json


def enable(task_dir: str, mode: str = "human-assisted", realism: str = "balanced") -> dict:
    td = Path(task_dir)
    state = load_json(str(td / "human_mode.json"), default={})
    state.update({
        "enabled": True,
        "mode": mode,
        "realism": realism,
        "policies": {
            "pauseOnLogin": True,
            "pauseOnMfa": True,
            "pauseOnCaptcha": True,
            "pauseOnApproval": True,
            "preferVisibleUiTransitions": True,
            "preferStepwiseNavigation": True,
            "avoidBypassBehavior": True,
        }
    })
    save_json(str(td / "human_mode.json"), state)
    return state


def build_interaction_plan(task_dir: str) -> dict:
    td = Path(task_dir)
    device = load_json(str(td / "device_profile.json"), default={})
    human_mode = load_json(str(td / "human_mode.json"), default={})
    interaction = {
        "deviceProfile": device.get("name", "desktop-default"),
        "viewport": device.get("viewport", {}),
        "delayMs": device.get("interactionStyle", {}).get("delayMs", 120),
        "scrollStep": device.get("interactionStyle", {}).get("scrollStep", 700),
        "typingSlowly": device.get("interactionStyle", {}).get("typingSlowly", False),
        "realism": human_mode.get("realism", "balanced"),
        "notes": [
            "Use explicit page transitions instead of hidden shortcuts when practical.",
            "Keep actions ordered and observable.",
            "Pause for human handoff on protected checkpoints instead of forcing through them."
        ]
    }
    save_json(str(td / "interaction_plan.json"), interaction)
    return interaction


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: browser_human_mode.py <enable|plan> <task_dir> [args...]", file=sys.stderr)
        raise SystemExit(1)
    cmd = sys.argv[1]
    if cmd == "enable":
        mode = sys.argv[3] if len(sys.argv) > 3 else "human-assisted"
        realism = sys.argv[4] if len(sys.argv) > 4 else "balanced"
        print(json.dumps(enable(sys.argv[2], mode, realism), ensure_ascii=False, indent=2))
    elif cmd == "plan":
        print(json.dumps(build_interaction_plan(sys.argv[2]), ensure_ascii=False, indent=2))
    else:
        raise SystemExit(f"unknown command: {cmd}")
