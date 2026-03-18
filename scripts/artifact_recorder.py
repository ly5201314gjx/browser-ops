#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from state_store import load_json, save_json


def record_artifact(task_dir: str, kind: str, path: str, url: str = "", note: str = "") -> dict:
    td = Path(task_dir)
    manifest_path = td / "artifacts_manifest.json"
    manifest = load_json(str(manifest_path), default={"artifacts": []})
    entry = {
        "ts": datetime.now().isoformat(),
        "kind": kind,
        "path": path,
        "url": url,
        "note": note,
    }
    manifest.setdefault("artifacts", []).append(entry)
    save_json(str(manifest_path), manifest)
    return entry


def record_failure_artifact(task_dir: str, url: str, reason: str, snapshot_path: str = "", screenshot_path: str = "") -> dict:
    td = Path(task_dir)
    failure_path = td / "failure_artifacts.json"
    failures = load_json(str(failure_path), default=[])
    entry = {
        "ts": datetime.now().isoformat(),
        "url": url,
        "reason": reason,
        "snapshotPath": snapshot_path,
        "screenshotPath": screenshot_path,
    }
    failures.append(entry)
    save_json(str(failure_path), failures)
    return entry


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: artifact_recorder.py <artifact|failure> <task_dir> ...", file=sys.stderr)
        raise SystemExit(1)
    mode = sys.argv[1]
    if mode == "artifact":
        kind = sys.argv[3]
        path = sys.argv[4]
        url = sys.argv[5] if len(sys.argv) > 5 else ""
        note = sys.argv[6] if len(sys.argv) > 6 else ""
        print(json.dumps(record_artifact(sys.argv[2], kind, path, url, note), ensure_ascii=False))
    elif mode == "failure":
        url = sys.argv[3]
        reason = sys.argv[4]
        snapshot = sys.argv[5] if len(sys.argv) > 5 else ""
        screenshot = sys.argv[6] if len(sys.argv) > 6 else ""
        print(json.dumps(record_failure_artifact(sys.argv[2], url, reason, snapshot, screenshot), ensure_ascii=False))
    else:
        raise SystemExit(f"unknown mode: {mode}")
