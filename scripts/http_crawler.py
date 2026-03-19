#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from browser_ops.execution.http_crawler import LinkCollector, crawl_detail, crawl_list, fallback_extract_detail, fallback_extract_links, fetch, main, same_domain

__all__ = [
    "LinkCollector",
    "crawl_detail",
    "crawl_list",
    "fallback_extract_detail",
    "fallback_extract_links",
    "fetch",
    "main",
    "same_domain",
]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: http_crawler.py <profile.json> <task_dir> [list|detail]", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "list")
