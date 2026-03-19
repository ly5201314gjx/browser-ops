#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.execution.browser_page_processor import extract_next_url_from_items, main, parse_snapshot_items, process_snapshot

__all__ = ["extract_next_url_from_items", "main", "parse_snapshot_items", "process_snapshot"]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
