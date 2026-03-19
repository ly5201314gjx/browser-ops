#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def classify_page(text: str) -> str:
    lower = text.lower()
    score = {
        "list": 0,
        "detail": 0,
        "login": 0,
        "search": 0,
        "dashboard": 0,
    }

    if re.search(r'\bmore\b|\bnext\b|\bpagination\b|\bpage\s*\d+', lower):
        score["list"] += 2
    if len(re.findall(r'link\s+"', text)) >= 8:
        score["list"] += 2
    if re.search(r'heading\s+"', text):
        score["detail"] += 1
    if len(re.findall(r'paragraph', lower)) >= 3:
        score["detail"] += 2
    if re.search(r'search|results for|filter|sort by', lower):
        score["search"] += 2
    if re.search(r'dashboard|settings|analytics|admin', lower):
        score["dashboard"] += 2

    checkpoints = detect_human_checkpoints(text)
    if checkpoints.get("login") and (checkpoints.get("passwordField") or checkpoints.get("authFlowSignals", 0) >= 2):
        score["login"] += 4

    return max(score, key=score.get)


def detect_embedded_json(text: str) -> dict:
    signals = {
        "nextData": "__NEXT_DATA__" in text,
        "nuxt": "__NUXT__" in text,
        "jsonScript": bool(re.search(r'application/json', text, re.I)),
        "ldJson": bool(re.search(r'ld\+json', text, re.I)),
    }
    signals["present"] = any(signals.values())
    return signals


def detect_human_checkpoints(text: str) -> dict:
    lower = text.lower()
    password_field = bool(re.search(r'password|passcode', lower))
    sign_in_phrase = bool(re.search(r'sign in|log in|sign into your account|enter your password', lower))
    verify_phrase = bool(re.search(r'verification code|authenticator|two-factor|2fa|mfa', lower))
    captcha = bool(re.search(r'captcha|verify you are human|robot check', lower))
    approval = bool(re.search(r'approve|consent|allow access|grant access', lower))
    login_link_only = bool(re.search(r'link\s+"login"', text, re.I))

    login = False
    auth_flow_signals = sum([password_field, sign_in_phrase, verify_phrase])
    if password_field or sign_in_phrase or verify_phrase:
        login = True
    elif login_link_only and auth_flow_signals >= 1:
        login = True

    return {
        "captcha": captcha,
        "mfa": verify_phrase,
        "login": login,
        "approval": approval,
        "passwordField": password_field,
        "authFlowSignals": auth_flow_signals,
        "loginLinkOnly": login_link_only,
    }


def extract_link_candidates(text: str, base_url: str) -> list[dict]:
    items = []
    current_title = None
    idx = 0
    for line in text.splitlines():
        clean = line.strip()
        mt = re.search(r'link\s+"([^"]+)"', clean)
        if mt:
            current_title = mt.group(1).strip()
        mu = re.search(r'/url:\s*"?(https?://[^\s"]+|\?[^\s"]+|/[^\s"]+)"?', clean)
        if mu:
            raw = mu.group(1).rstrip('),.;"')
            if raw.startswith('?'):
                parsed = urlparse(base_url)
                url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}{raw}"
            elif raw.startswith('/'):
                parsed = urlparse(base_url)
                url = f"{parsed.scheme}://{parsed.netloc}{raw}"
            else:
                url = raw
            items.append({"index": idx, "title": current_title or url, "url": url})
            idx += 1
            current_title = None
    out = []
    seen = set()
    for item in items:
        if item['url'] in seen:
            continue
        seen.add(item['url'])
        out.append(item)
    return out


def detect_pagination(items: list[dict]) -> dict:
    candidates = []
    for item in items:
        t = item.get("title", "").lower()
        u = item.get("url", "")
        if t in {"more", "next", "older", "下一页"} or re.search(r'[?&]p=\d+', u):
            candidates.append(item)
    return {
        "detected": bool(candidates),
        "candidates": candidates[:10],
    }


def recommend_route(page_type: str, embedded: dict, checkpoints: dict, pagination: dict) -> str:
    if checkpoints.get("captcha") or checkpoints.get("mfa") or checkpoints.get("approval"):
        return "human"
    if checkpoints.get("login"):
        return "human"
    if embedded.get("present"):
        return "hybrid"
    if page_type in {"list", "dashboard", "search"} and pagination.get("detected"):
        return "browser"
    if page_type == "detail":
        return "browser"
    return "http"


def build_selector_hints(items: list[dict], page_type: str) -> dict:
    hints = {
        "pageType": page_type,
        "candidateCount": len(items),
        "suggestions": []
    }
    if page_type == "list":
        hints["suggestions"] = [
            "look for repeated link/title blocks",
            "prefer row/card/article containers",
            "detect explicit next-page links before guessing URL patterns",
        ]
    elif page_type == "detail":
        hints["suggestions"] = [
            "prefer heading + paragraph blocks",
            "look for main/article/content region",
            "extract author/time only if confidently present",
        ]
    return hints


def analyze(snapshot_path: str, base_url: str) -> dict:
    text = Path(snapshot_path).read_text(encoding="utf-8")
    page_type = classify_page(text)
    embedded = detect_embedded_json(text)
    checkpoints = detect_human_checkpoints(text)
    links = extract_link_candidates(text, base_url)
    pagination = detect_pagination(links)
    route = recommend_route(page_type, embedded, checkpoints, pagination)
    hints = build_selector_hints(links, page_type)

    report = {
        "ok": True,
        "baseUrl": base_url,
        "pageType": page_type,
        "recommendedRoute": route,
        "embeddedJson": embedded,
        "humanCheckpoints": checkpoints,
        "pagination": pagination,
        "candidateLinks": links[:30],
        "selectorHints": hints,
    }
    return report


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: site_intelligence.py <snapshot.txt> <base_url>", file=sys.stderr)
        return 1
    report = analyze(argv[1], argv[2])
    out = Path(argv[1]).with_suffix('.intel.json')
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({"ok": True, "output": str(out), "pageType": report['pageType'], "recommendedRoute": report['recommendedRoute']}, ensure_ascii=False))
    return 0
