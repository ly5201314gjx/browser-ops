#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.orchestration.browser_ops_orchestrator import (
    advance_phase,
    append_note,
    init_run,
    main,
    next_action,
    status,
)

__all__ = ["advance_phase", "append_note", "init_run", "main", "next_action", "status"]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
