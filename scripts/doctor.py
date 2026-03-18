#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
PROFILE = ROOT / "assets" / "example_profiles" / "hackernews-browser.json"
REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "SKILL.md",
    PROFILE,
    SCRIPTS / "browser_ops_orchestrator.py",
    SCRIPTS / "browser_runbook_builder.py",
    SCRIPTS / "action_policy_engine.py",
    SCRIPTS / "browser_handoff_payload.py",
    SCRIPTS / "failure_recovery_engine.py",
]

def check_python() -> dict:
    return {
        "ok": sys.version_info >= (3, 10),
        "python": sys.version.split()[0],
        "required": ">=3.10",
    }

def check_files() -> list[dict]:
    return [{"path": str(p.relative_to(ROOT)), "ok": p.exists()} for p in REQUIRED_FILES]

def check_profile() -> dict:
    try:
        data = json.loads(PROFILE.read_text(encoding="utf-8"))
        ok = all(k in data for k in ("name", "route", "startUrls"))
        return {"ok": ok, "profile": data.get("name", "unknown")}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def check_imports() -> list[dict]:
    out = []
    for path in sorted(SCRIPTS.glob("*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        out.append({"module": path.name, "ok": spec is not None})
    return out

def main() -> int:
    report = {
        "python": check_python(),
        "files": check_files(),
        "profile": check_profile(),
        "imports": check_imports(),
        "cwdWritable": os.access(str(ROOT), os.W_OK),
    }
    all_ok = report["python"]["ok"] and report["profile"]["ok"] and all(x["ok"] for x in report["files"])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if not all_ok:
        return 1
    print("\n✅ doctor check passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
