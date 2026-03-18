#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXCLUDE_DIRS = {"__pycache__", "logs"}
EXCLUDE_SUFFIXES = {".pyc"}


def copy_filtered(src: Path, dst: Path) -> None:
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if path.suffix in EXCLUDE_SUFFIXES:
            continue
        target = dst / rel
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def main(skill_dir: str, output_dir: str) -> int:
    src = Path(skill_dir).resolve()
    out = Path(output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="browser_ops_clean_pkg_") as tmp:
        tmp_path = Path(tmp)
        staged = tmp_path / src.name
        staged.mkdir(parents=True, exist_ok=True)
        copy_filtered(src, staged)

        pkg_script = Path("/home/lg030452/.npm-global/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py")
        cmd = [sys.executable, str(pkg_script), str(staged), str(out)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        return proc.returncode


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: build_clean_package.py <skill_dir> <output_dir>", file=sys.stderr)
        raise SystemExit(1)
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
