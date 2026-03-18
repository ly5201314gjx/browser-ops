#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from state_store import load_json, save_json


def bootstrap(task_dir: str, snapshot_path: str, base_url: str) -> dict:
    td = Path(task_dir).resolve()
    base = Path(__file__).resolve().parent
    intel_script = base / "site_intelligence.py"
    profile_script = base / "profile_suggester.py"

    intel_proc = subprocess.run(
        [sys.executable, str(intel_script), snapshot_path, base_url],
        capture_output=True,
        text=True,
    )
    if intel_proc.returncode != 0:
        raise SystemExit(intel_proc.stderr or intel_proc.stdout)

    intel_out = Path(snapshot_path).with_suffix('.intel.json')
    profile_proc = subprocess.run(
        [sys.executable, str(profile_script), str(intel_out)],
        capture_output=True,
        text=True,
    )
    if profile_proc.returncode != 0:
        raise SystemExit(profile_proc.stderr or profile_proc.stdout)

    intel_data = load_json(str(intel_out), default={})
    profile_out = intel_out.with_suffix('.profile.json')
    profile_data = load_json(str(profile_out), default={})

    orchestrator = load_json(str(td / "orchestrator_state.json"), default={})
    orchestrator["intelligence"] = {
        "snapshotPath": str(Path(snapshot_path).resolve()),
        "intelPath": str(intel_out.resolve()),
        "profileDraftPath": str(profile_out.resolve()),
        "pageType": intel_data.get("pageType"),
        "recommendedRoute": intel_data.get("recommendedRoute"),
    }
    orchestrator.setdefault("notes", []).append({
        "kind": "intelligence-bootstrap",
        "pageType": intel_data.get("pageType"),
        "recommendedRoute": intel_data.get("recommendedRoute"),
    })
    save_json(str(td / "orchestrator_state.json"), orchestrator)

    return {
        "ok": True,
        "intelPath": str(intel_out),
        "profileDraftPath": str(profile_out),
        "pageType": intel_data.get("pageType"),
        "recommendedRoute": intel_data.get("recommendedRoute"),
        "profileName": profile_data.get("name"),
    }


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: intelligence_bootstrap.py <task_dir> <snapshot.txt> <base_url>", file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps(bootstrap(sys.argv[1], sys.argv[2], sys.argv[3]), ensure_ascii=False))
