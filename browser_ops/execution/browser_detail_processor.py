#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from browser_ops.core.state_store import append_jsonl, load_json, save_json


def parse_detail_snapshot(text: str, url: str) -> dict:
    lines = [x.strip() for x in text.splitlines() if x.strip()]

    title = ""
    for line in lines:
        m = re.search(r'heading\s+"([^"]+)"', line, re.I)
        if m:
            title = m.group(1).strip()
            break
    if not title:
        for line in lines:
            m = re.search(r'link\s+"([^"]{12,})"', line, re.I)
            if m:
                title = m.group(1).strip()
                break

    paragraphs = []
    for line in lines:
        m = re.search(r'paragraph(?:\s+\[[^\]]+\])?:\s*(.*)$', line, re.I)
        if m:
            txt = m.group(1).strip()
            if txt:
                paragraphs.append(txt)

    text_blob = "\n\n".join(paragraphs[:12])

    links = []
    pending_title = None
    for line in lines:
        mt = re.search(r'link\s+"([^"]+)"', line)
        if mt:
            pending_title = mt.group(1).strip()
        mu = re.search(r'/url:\s*(https?://\S+)', line)
        if mu:
            u = mu.group(1).rstrip('),.;')
            links.append({"title": pending_title or u, "url": u})
            pending_title = None

    return {
        "url": url,
        "title": title,
        "content": text_blob,
        "outLinks": links[:50],
        "contentLength": len(text_blob),
    }


def record_detail(task_dir: str, snapshot_path: str, url: str, source_item_link: str = "") -> dict:
    td = Path(task_dir)
    text = Path(snapshot_path).read_text(encoding="utf-8")
    detail = parse_detail_snapshot(text, url)
    if source_item_link:
        detail["sourceItemLink"] = source_item_link
    append_jsonl(str(td / "detail_results.jsonl"), detail)

    runtime = load_json(str(td / "browser_runtime.json"), default={})
    runtime["detailsExtracted"] = runtime.get("detailsExtracted", 0) + 1
    runtime["lastDetailUrl"] = url
    runtime["status"] = "running"
    save_json(str(td / "browser_runtime.json"), runtime)
    save_json(str(td / "last_detail.json"), detail)

    return {"ok": True, "taskDir": str(td), "detailTitle": detail.get("title", ""), "contentLength": detail.get("contentLength", 0)}


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print('Usage: browser_detail_processor.py <task_dir> <snapshot.txt> <url> [source_item_link]', file=sys.stderr)
        return 1
    src = argv[4] if len(argv) > 4 else ""
    print(json.dumps(record_detail(argv[1], argv[2], argv[3], src), ensure_ascii=False))
    return 0
