#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.intelligence.site_intelligence import (
    analyze,
    build_selector_hints,
    classify_page,
    detect_embedded_json,
    detect_human_checkpoints,
    detect_pagination,
    extract_link_candidates,
    main,
    recommend_route,
)

__all__ = [
    "analyze",
    "build_selector_hints",
    "classify_page",
    "detect_embedded_json",
    "detect_human_checkpoints",
    "detect_pagination",
    "extract_link_candidates",
    "main",
    "recommend_route",
]


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
