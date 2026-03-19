#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.control.autopilot_tick import main, tick

__all__ = ["main", "tick"]


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
