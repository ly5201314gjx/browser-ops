#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from typing import Any
from urllib.parse import urljoin


def pick_text(node) -> str:
    if node is None:
        return ""
    return " ".join(node.get_text(" ", strip=True).split())


def pick_attr(node, attr: str) -> str:
    if node is None:
        return ""
    return (node.get(attr) or "").strip()


def select_first(soup, selector: str):
    if not selector:
        return None
    return soup.select_one(selector)


def select_all(soup, selector: str):
    if not selector:
        return []
    return soup.select(selector)


def extract_link(base_url: str, node, selector: str) -> str:
    target = node.select_one(selector) if selector else node
    if target is None:
        return ""
    href = target.get("href") or ""
    return urljoin(base_url, href)


def extract_items_from_list(soup, base_url: str, list_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    item_selector = list_cfg.get("itemSelector")
    items = []
    for idx, node in enumerate(select_all(soup, item_selector)):
        title_node = node.select_one(list_cfg.get("titleSelector", "")) if list_cfg.get("titleSelector") else None
        summary_node = node.select_one(list_cfg.get("summarySelector", "")) if list_cfg.get("summarySelector") else None
        title = pick_text(title_node) or pick_text(node)
        link = extract_link(base_url, node, list_cfg.get("linkSelector", ""))
        summary = pick_text(summary_node)
        if not title and not link:
            continue
        items.append({
            "index": idx,
            "title": title,
            "link": link,
            "summary": summary,
            "source": base_url,
        })
    return items


def extract_next_page(soup, base_url: str, list_cfg: dict[str, Any]) -> str:
    next_selector = list_cfg.get("nextPageSelector")
    if not next_selector:
        return ""
    node = soup.select_one(next_selector)
    if node is None:
        return ""
    href = node.get("href") or ""
    return urljoin(base_url, href)


def extract_detail(soup, base_url: str, detail_cfg: dict[str, Any]) -> dict[str, Any]:
    def text(selector: str) -> str:
        return pick_text(select_first(soup, selector))

    tags = [pick_text(n) for n in select_all(soup, detail_cfg.get("tagSelector", ""))]
    data = {
        "url": base_url,
        "title": text(detail_cfg.get("titleSelector", "")),
        "content": text(detail_cfg.get("contentSelector", "")),
        "time": text(detail_cfg.get("timeSelector", "")),
        "author": text(detail_cfg.get("authorSelector", "")),
        "tags": [t for t in tags if t],
    }
    return data


def find_embedded_json(html: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    patterns = [
        r"<script[^>]*id=\"__NEXT_DATA__\"[^>]*>(.*?)</script>",
        r"<script[^>]*type=\"application/json\"[^>]*>(.*?)</script>",
    ]
    for pat in patterns:
        for m in re.finditer(pat, html, re.S | re.I):
            raw = m.group(1).strip()
            try:
                found.append(json.loads(raw))
            except Exception:
                continue
    return found
