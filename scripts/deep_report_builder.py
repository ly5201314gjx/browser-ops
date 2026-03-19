#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.deep_analysis.deep_report_builder import build_report, main

__all__ = ["build_report", "main"]


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
