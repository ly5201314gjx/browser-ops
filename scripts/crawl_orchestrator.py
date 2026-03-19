#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.execution.crawl_orchestrator import initialize, main

__all__ = ["initialize", "main"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: crawl_orchestrator.py <profile.json> [out_dir]", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
