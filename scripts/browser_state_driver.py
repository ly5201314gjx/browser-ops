#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.control.browser_state_driver import complete, init_runtime, load_plan, main, record_failure, record_page

__all__ = ["complete", "init_runtime", "load_plan", "main", "record_failure", "record_page"]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
