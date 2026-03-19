#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.execution.detail_batch_driver import init_batch, main, mark_done, mark_fail, next_item

__all__ = ["init_batch", "main", "mark_done", "mark_fail", "next_item"]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
