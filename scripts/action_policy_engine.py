#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.policy.action_policy_engine import build_action_policy, main

__all__ = ["build_action_policy", "main"]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
