#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.recovery.failure_recovery_engine import (
    build_recovery_plan,
    bump_retry,
    classify_failure,
    main,
    register_failure,
    resolve_incident,
    status,
)

__all__ = [
    "build_recovery_plan",
    "bump_retry",
    "classify_failure",
    "main",
    "register_failure",
    "resolve_incident",
    "status",
]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
