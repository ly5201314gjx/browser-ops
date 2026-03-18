#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from state_store import save_json

DEVICE_PROFILES = {
    "desktop-default": {
        "label": "Desktop Default",
        "viewport": {"width": 1440, "height": 900},
        "userAgentHint": "desktop",
        "interactionStyle": {
            "delayMs": 120,
            "scrollStep": 700,
            "typingSlowly": False
        }
    },
    "mobile-default": {
        "label": "Mobile Default",
        "viewport": {"width": 390, "height": 844},
        "userAgentHint": "mobile",
        "interactionStyle": {
            "delayMs": 180,
            "scrollStep": 520,
            "typingSlowly": True
        }
    },
    "tablet-default": {
        "label": "Tablet Default",
        "viewport": {"width": 820, "height": 1180},
        "userAgentHint": "tablet",
        "interactionStyle": {
            "delayMs": 150,
            "scrollStep": 620,
            "typingSlowly": True
        }
    }
}


def apply_profile(task_dir: str, profile_name: str) -> dict:
    td = Path(task_dir)
    profile = DEVICE_PROFILES.get(profile_name)
    if not profile:
        raise SystemExit(f"unknown device profile: {profile_name}")
    out = {
        "name": profile_name,
        **profile,
    }
    save_json(str(td / "device_profile.json"), out)
    return out


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: device_profile_manager.py <task_dir> <profile_name>", file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(apply_profile(sys.argv[1], sys.argv[2]), ensure_ascii=False, indent=2))
