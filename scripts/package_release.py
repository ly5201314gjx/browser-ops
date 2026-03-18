#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
NAME = "browser-ops-openclaw-v0.1.1"

INCLUDE = [
    "README.md",
    "LICENSE",
    "SKILL.md",
    "pyproject.toml",
    "requirements.txt",
    "install.sh",
    "demo.sh",
    "ROADMAP.md",
    "docs",
    "assets",
    "references",
    "scripts",
]


def main() -> int:
    DIST.mkdir(exist_ok=True)
    stage = DIST / NAME
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    for item in INCLUDE:
        src = ROOT / item
        dst = stage / item
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
            for pycache in dst.rglob("__pycache__"):
                shutil.rmtree(pycache, ignore_errors=True)
            for pyc in dst.rglob("*.pyc"):
                pyc.unlink(missing_ok=True)
        elif src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    zip_path = shutil.make_archive(str(DIST / NAME), "zip", root_dir=DIST, base_dir=NAME)
    tar_path = shutil.make_archive(str(DIST / NAME), "gztar", root_dir=DIST, base_dir=NAME)
    print(f"Created: {zip_path}")
    print(f"Created: {tar_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
