#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import requests

from extractors import find_embedded_json
from profile_runner import load_profile
from state_store import append_jsonl, load_json, save_json

USER_AGENT = "Mozilla/5.0 (compatible; BrowserOps/1.0; +OpenClaw)"


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._in_a = False
        self._href = ""
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "a":
            self._in_a = True
            self._buf = []
            self._href = dict(attrs).get("href", "")

    def handle_data(self, data):
        if self._in_a:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "a" and self._in_a:
            text = " ".join("".join(self._buf).split())
            self.links.append({"title": text, "link": self._href})
            self._in_a = False
            self._href = ""
            self._buf = []


def fetch(url: str, timeout: int = 20) -> requests.Response:
    return requests.get(url, timeout=timeout, headers={"User-Agent": USER_AGENT})


def same_domain(url: str, allowed_domains: list[str]) -> bool:
    host = urlparse(url).netloc
    return any(host == d or host.endswith('.' + d) for d in allowed_domains)


def fallback_extract_links(base_url: str, html: str) -> list[dict]:
    p = LinkCollector()
    p.feed(html)
    items = []
    for idx, item in enumerate(p.links):
        href = item.get("link") or ""
        if not href:
            continue
        if href.startswith("#"):
            continue
        if href.startswith("/"):
            href = base_url.rstrip("/") + href
        items.append({
            "index": idx,
            "title": item.get("title") or href,
            "link": href,
            "summary": "",
            "source": base_url,
        })
    return items


def fallback_extract_detail(url: str, html: str) -> dict:
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if m:
        title = " ".join(m.group(1).split())
    text = re.sub(r"<script.*?</script>", " ", html, flags=re.I | re.S)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    text = " ".join(text.split())[:4000]
    return {"url": url, "title": title, "content": text, "time": "", "author": "", "tags": []}


def crawl_list(profile: dict, task_dir: Path):
    state_file = task_dir / "state.json"
    state = load_json(str(state_file), default={})
    queue = state.get("queue", list(profile.get("startUrls", [])))
    visited = set(state.get("visited", []))
    max_pages = profile.get("maxPages", 20)
    rate_ms = profile.get("rateLimitMs", 1200)
    allowed_domains = profile.get("allowedDomains", [])

    pages = state.get("pagesVisited", 0)
    while queue and pages < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        if allowed_domains and not same_domain(url, allowed_domains):
            state.setdefault("failedUrls", []).append({"url": url, "reason": "domain-not-allowed"})
            continue
        try:
            resp = fetch(url)
            resp.raise_for_status()
            html = resp.text
            embedded = find_embedded_json(html)
            if embedded:
                save_json(str(task_dir / f"embedded_{pages+1}.json"), embedded)

            items = fallback_extract_links(url, html)
            for item in items:
                append_jsonl(str(task_dir / "results.jsonl"), item)

            visited.add(url)
            pages += 1
            state["visited"] = list(visited)
            state["queue"] = queue
            state["pagesVisited"] = pages
            state["itemsExtracted"] = state.get("itemsExtracted", 0) + len(items)
            state["status"] = "running"
            save_json(str(state_file), state)
            time.sleep(rate_ms / 1000)
        except Exception as e:
            state.setdefault("failedUrls", []).append({"url": url, "reason": str(e)})
            save_json(str(state_file), state)

    state["status"] = "completed"
    save_json(str(state_file), state)
    print(json.dumps({
        "ok": True,
        "pagesVisited": state.get("pagesVisited", 0),
        "itemsExtracted": state.get("itemsExtracted", 0),
        "taskDir": str(task_dir)
    }, ensure_ascii=False))


def crawl_detail(profile: dict, task_dir: Path, urls: list[str]):
    out = task_dir / "detail_results.jsonl"
    for url in urls:
        try:
            resp = fetch(url)
            resp.raise_for_status()
            detail = fallback_extract_detail(url, resp.text)
            append_jsonl(str(out), detail)
        except Exception as e:
            state = load_json(str(task_dir / "state.json"), default={})
            state.setdefault("failedUrls", []).append({"url": url, "reason": str(e)})
            save_json(str(task_dir / "state.json"), state)


def main(profile_path: str, task_dir: str, mode: str = "list"):
    profile = load_profile(profile_path)
    td = Path(task_dir)
    td.mkdir(parents=True, exist_ok=True)
    if mode == "list":
        crawl_list(profile, td)
    elif mode == "detail":
        results = []
        p = td / "results.jsonl"
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    results.append(json.loads(line))
        urls = [x.get("link") for x in results if x.get("link")]
        crawl_detail(profile, td, urls)
        print(json.dumps({"ok": True, "detailUrls": len(urls), "taskDir": str(td)}, ensure_ascii=False))
    else:
        raise SystemExit("mode must be list or detail")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: http_crawler.py <profile.json> <task_dir> [list|detail]", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "list")
