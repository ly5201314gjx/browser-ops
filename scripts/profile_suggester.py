#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse


def suggest(intel_path: str) -> dict:
    data = json.loads(Path(intel_path).read_text(encoding="utf-8"))
    base_url = data.get("baseUrl", "")
    parsed = urlparse(base_url)
    name = parsed.netloc.replace('.', '-') or 'site-profile'
    page_type = data.get("pageType", "list")
    route = data.get("recommendedRoute", "browser")
    pagination = data.get("pagination", {})

    profile = {
        "name": name,
        "route": route,
        "startUrls": [base_url],
        "allowedDomains": [parsed.netloc] if parsed.netloc else [],
        "requiresLogin": data.get("humanCheckpoints", {}).get("login", False),
        "humanCheckpoints": data.get("humanCheckpoints", {}),
        "rateLimitMs": 1200,
        "maxPages": 3,
        "list": {
            "itemSelector": "",
            "fallbackItemSelectors": [],
            "titleSelector": "",
            "linkSelector": "",
            "summarySelector": "",
            "nextPageSelector": ""
        },
        "detail": {
            "titleSelector": "",
            "contentSelector": "",
            "timeSelector": "",
            "authorSelector": "",
            "tagSelector": ""
        },
        "extraction": {
            "preferEmbeddedJson": data.get("embeddedJson", {}).get("present", False),
            "preferNetworkDiscovery": route == "hybrid",
            "captureScreenshotsOnFailure": True,
            "outputFormat": "jsonl"
        },
        "intelHints": data.get("selectorHints", {}),
    }

    if page_type == 'list' and pagination.get('detected'):
        cands = pagination.get('candidates', [])
        if cands:
            profile['list']['nextPageSelector'] = f"candidate:{cands[0].get('title', 'next')}"

    return profile


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: profile_suggester.py <snapshot.intel.json>', file=sys.stderr)
        raise SystemExit(1)
    profile = suggest(sys.argv[1])
    out = Path(sys.argv[1]).with_suffix('.profile.json')
    out.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({"ok": True, "output": str(out), "name": profile['name'], "route": profile['route']}, ensure_ascii=False))
