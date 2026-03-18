#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

from state_store import load_json, save_json


DEFAULT_POLICIES = {
    "desktop-default": {
        "device": "desktop-default",
        "timing": {
            "firstPaintPauseMs": [500, 1400],
            "elementConfirmPauseMs": [220, 700],
            "betweenActionsMs": [180, 600],
            "pageSettleMs": [1000, 2600],
            "readingPauseMs": [1800, 6000],
        },
        "touch": {
            "downDelayMs": [70, 180],
            "tapHoldMs": [50, 120],
            "longPressMs": [320, 800],
            "multiTouchGapMs": [35, 110],
        },
        "motion": {
            "swipeDurationMs": [280, 900],
            "horizontalOffsetPx": [3, 14],
            "verticalJitterPx": [2, 10],
            "inertia": [0.84, 0.93],
            "postScrollPauseMs": [220, 700],
        },
        "randomization": {
            "timeJitterPct": [8, 16],
            "coordinateJitterPx": [2, 10],
        },
    },
    "mobile-default": {
        "device": "mobile-default",
        "timing": {
            "firstPaintPauseMs": [600, 1800],
            "elementConfirmPauseMs": [300, 900],
            "betweenActionsMs": [200, 850],
            "pageSettleMs": [1200, 3200],
            "readingPauseMs": [2000, 8000],
        },
        "touch": {
            "downDelayMs": [80, 220],
            "tapHoldMs": [60, 140],
            "longPressMs": [350, 900],
            "multiTouchGapMs": [40, 130],
        },
        "motion": {
            "swipeDurationMs": [320, 1100],
            "horizontalOffsetPx": [4, 18],
            "verticalJitterPx": [2, 12],
            "inertia": [0.82, 0.93],
            "postScrollPauseMs": [250, 900],
        },
        "randomization": {
            "timeJitterPct": [8, 18],
            "coordinateJitterPx": [3, 12],
        },
    },
    "tablet-default": {
        "device": "tablet-default",
        "timing": {
            "firstPaintPauseMs": [550, 1600],
            "elementConfirmPauseMs": [260, 820],
            "betweenActionsMs": [190, 760],
            "pageSettleMs": [1100, 2900],
            "readingPauseMs": [1900, 7000],
        },
        "touch": {
            "downDelayMs": [75, 210],
            "tapHoldMs": [55, 130],
            "longPressMs": [340, 860],
            "multiTouchGapMs": [38, 120],
        },
        "motion": {
            "swipeDurationMs": [300, 1000],
            "horizontalOffsetPx": [4, 16],
            "verticalJitterPx": [2, 11],
            "inertia": [0.83, 0.93],
            "postScrollPauseMs": [240, 800],
        },
        "randomization": {
            "timeJitterPct": [8, 17],
            "coordinateJitterPx": [3, 11],
        },
    },
}


def build_policy(task_dir: str, device: str | None = None) -> dict:
    td = Path(task_dir)
    device_profile = load_json(str(td / "device_profile.json"), default={})
    profile_name = device or device_profile.get("name") or "mobile-default"
    policy = DEFAULT_POLICIES.get(profile_name, DEFAULT_POLICIES["mobile-default"])
    save_json(str(td / "interaction_policy.json"), policy)
    return policy


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: interaction_policy_engine.py <task_dir> [device_profile]", file=sys.stderr)
        raise SystemExit(1)
    result = build_policy(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None)
    print(json.dumps(result, ensure_ascii=False, indent=2))
