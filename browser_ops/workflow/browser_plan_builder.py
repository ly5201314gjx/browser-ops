#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from action_policy_engine import build_action_policy
from browser_ops.core.profile_runner import load_profile
from browser_ops.core.state_store import save_json


def build_plan(profile: dict, task_dir: Path) -> dict:
    start_url = profile.get("startUrls", [""])[0]
    action_policy = build_action_policy(str(task_dir), str(task_dir / "resolved_profile.json"))
    interaction = action_policy.get("interactionPolicy", {})
    plan = {
        "createdAt": datetime.now().isoformat(),
        "profile": profile.get("name"),
        "route": profile.get("route", "browser"),
        "device": action_policy.get("device"),
        "navigationStyle": action_policy.get("navigationStyle"),
        "riskTolerance": action_policy.get("riskTolerance"),
        "interactionPolicy": interaction,
        "steps": [
            {
                "kind": "open",
                "url": start_url,
                "settleMs": interaction.get("timing", {}).get("pageSettleMs", [1200, 3200]),
            },
            {
                "kind": "snapshot",
                "note": "capture initial page structure",
                "pauseBeforeMs": interaction.get("timing", {}).get("elementConfirmPauseMs", [300, 900]),
            },
            {
                "kind": "extract_list",
                "itemSelector": profile.get("list", {}).get("itemSelector"),
                "titleSelector": profile.get("list", {}).get("titleSelector"),
                "linkSelector": profile.get("list", {}).get("linkSelector"),
                "summarySelector": profile.get("list", {}).get("summarySelector"),
                "pauseAfterMs": interaction.get("timing", {}).get("betweenActionsMs", [200, 850]),
            },
            {
                "kind": "paginate",
                "nextPageSelector": profile.get("list", {}).get("nextPageSelector"),
                "maxPages": profile.get("maxPages", 20),
                "rateLimitMs": profile.get("rateLimitMs", 1200),
                "scrollPauseMs": interaction.get("motion", {}).get("postScrollPauseMs", [250, 900]),
            },
        ],
        "humanCheckpoints": profile.get("humanCheckpoints", {}),
        "checkpointPolicy": action_policy.get("checkpointPolicy", {}),
    }
    save_json(str(task_dir / "browser_plan.json"), plan)
    return plan


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: browser_plan_builder.py <profile.json> <task_dir>", file=sys.stderr)
        return 1
    profile = load_profile(argv[1])
    td = Path(argv[2])
    td.mkdir(parents=True, exist_ok=True)
    save_json(str(td / "resolved_profile.json"), profile)
    plan = build_plan(profile, td)
    print(json.dumps({"ok": True, "taskDir": str(td), "planPath": str(td / 'browser_plan.json'), "steps": len(plan['steps']), "device": plan.get('device')}, ensure_ascii=False))
    return 0
