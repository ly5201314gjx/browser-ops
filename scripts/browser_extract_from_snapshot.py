#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def parse_snapshot_text(text: str) -> list[dict]:
    items = []
    lines = text.splitlines()
    idx = 0
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        # Very loose MVP parser: lines containing markdown-like links or URL-ish patterns
        md = re.search(r"\[(.*?)\]\((https?://[^\)]+)\)", clean)
        if md:
            items.append({"index": idx, "title": md.group(1).strip(), "link": md.group(2).strip(), "summary": "", "source": "snapshot"})
            idx += 1
            continue
        urlm = re.search(r"(https?://\S+)", clean)
        if urlm:
            url = urlm.group(1).rstrip('),.;')
            title = clean.replace(urlm.group(1), '').strip(' -—:|') or url
            items.append({"index": idx, "title": title, "link": url, "summary": clean[:300], "source": "snapshot"})
            idx += 1
    # dedupe by link
    seen = set()
    out = []
    for item in items:
        link = item.get('link')
        if not link or link in seen:
            continue
        seen.add(link)
        out.append(item)
    return out


def main(path: str):
    p = Path(path)
    raw = p.read_text(encoding="utf-8")
    items = parse_snapshot_text(raw)
    out = p.with_suffix('.items.json')
    out.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({"ok": True, "items": len(items), "output": str(out)}, ensure_ascii=False))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: browser_extract_from_snapshot.py <snapshot.txt>', file=sys.stderr)
        raise SystemExit(1)
    main(sys.argv[1])
