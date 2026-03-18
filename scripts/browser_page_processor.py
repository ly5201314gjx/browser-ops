#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

from state_store import append_jsonl, load_json, save_json


def parse_snapshot_items(text: str, base_url: str) -> list[dict]:
    items = []
    idx = 0

    # Pattern A: multiline snapshot blocks
    lines = text.splitlines()
    current_title = None
    for i, line in enumerate(lines):
        clean = line.strip()
        m_title = re.search(r'link\s+"([^"]+)"', clean)
        if m_title:
            title = m_title.group(1).strip()
            # skip obvious nav/control links
            if title.lower() in {"upvote", "login", "more", "hacker news", "new", "past", "comments", "ask", "show", "jobs", "submit"}:
                current_title = None if title.lower() != 'more' else 'More'
            else:
                current_title = title
                continue

        m_url = re.search(r'/url:\s*"?(https?://[^\s"]+|\?[^\s"]+|[^\s"]+)"?', clean)
        if m_url:
            raw = m_url.group(1).rstrip('),.;"')
            url = urljoin(base_url, raw)
            title = current_title
            # detect explicit More link
            if 'More' in clean or title == 'More':
                items.append({"index": idx, "title": "More", "link": url, "summary": "pagination", "source": base_url, "kind": "pagination"})
                idx += 1
                current_title = None
                continue
            if title and url.startswith('http'):
                items.append({"index": idx, "title": title, "link": url, "summary": "", "source": base_url, "kind": "item"})
                idx += 1
                current_title = None

    # Pattern B: markdown-like fallback
    for clean in lines:
        md2 = re.search(r'\[(.*?)\]\((https?://[^\)]+)\)', clean)
        if md2:
            items.append({"index": idx, "title": md2.group(1).strip(), "link": md2.group(2).strip(), "summary": "", "source": base_url, "kind": "item"})
            idx += 1

    seen = set()
    out = []
    for item in items:
        key = (item.get("kind"), item.get("link"))
        if not item.get("link") or key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def extract_next_url_from_items(items: list[dict]) -> str:
    for item in items:
        if item.get('kind') == 'pagination' or item.get('title', '').strip().lower() == 'more':
            return item.get('link', '')
    return ''


def process_snapshot(task_dir: str, snapshot_path: str, base_url: str, note: str = "") -> dict:
    td = Path(task_dir)
    text = Path(snapshot_path).read_text(encoding='utf-8')
    runtime = load_json(str(td / 'browser_runtime.json'), default={})
    items = parse_snapshot_items(text, base_url)

    existing_links = set()
    results_path = td / 'results.jsonl'
    if results_path.exists():
        for line in results_path.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if obj.get('link'):
                    existing_links.add((obj.get('kind', 'item'), obj['link']))
            except Exception:
                pass

    new_items = []
    for item in items:
        key = (item.get('kind', 'item'), item['link'])
        if key in existing_links:
            continue
        new_items.append(item)
        append_jsonl(str(results_path), item)

    visited = runtime.setdefault('visitedUrls', [])
    if base_url not in visited:
        visited.append(base_url)
        runtime['pagesVisited'] = runtime.get('pagesVisited', 0) + 1
    runtime['itemsExtracted'] = runtime.get('itemsExtracted', 0) + len([x for x in new_items if x.get('kind') != 'pagination'])
    runtime['lastUrl'] = base_url
    runtime['lastNote'] = note or 'snapshot processed'
    runtime['status'] = 'running'

    next_url = extract_next_url_from_items(items)
    runtime['suggestedNextUrl'] = next_url
    save_json(str(td / 'browser_runtime.json'), runtime)
    (td / 'last_page_items.json').write_text(json.dumps(new_items, ensure_ascii=False, indent=2), encoding='utf-8')

    return {
        'ok': True,
        'baseUrl': base_url,
        'newItems': len([x for x in new_items if x.get('kind') != 'pagination']),
        'suggestedNextUrl': next_url,
        'taskDir': str(td),
    }


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: browser_page_processor.py <task_dir> <snapshot.txt> <base_url> [note]', file=sys.stderr)
        raise SystemExit(1)
    note = sys.argv[4] if len(sys.argv) > 4 else ''
    print(json.dumps(process_snapshot(sys.argv[1], sys.argv[2], sys.argv[3], note), ensure_ascii=False))
