#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.execution.browser_detail_processor import main, parse_detail_snapshot, record_detail

__all__ = ["main", "parse_detail_snapshot", "record_detail"]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
