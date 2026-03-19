#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

DEFAULT_HEADERS = {
    "User-Agent": "BrowserOpsConnectivity/0.1 (+OpenClaw)"
}


def _load_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _save_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _profile_connectivity(profile: dict) -> dict:
    return profile.get("connectivity", {})


def _candidate_urls(url: str, profile: dict) -> list[dict]:
    cfg = _profile_connectivity(profile)
    candidates = [{"mode": "direct", "url": url, "proxy": None}]

    for mirror in cfg.get("fallbackBaseUrls", []):
        parsed = urllib.parse.urlparse(url)
        path = parsed.path or "/"
        if parsed.query:
            path += f"?{parsed.query}"
        candidates.append({
            "mode": "mirror",
            "url": urllib.parse.urljoin(mirror.rstrip("/") + "/", path.lstrip("/")),
            "proxy": None,
        })

    proxy_env = cfg.get("proxyEnv")
    if proxy_env and os.getenv(proxy_env):
        candidates.append({
            "mode": "proxy",
            "url": url,
            "proxy": os.getenv(proxy_env),
            "proxyEnv": proxy_env,
        })
    return candidates


def _open(url: str, timeout: int, proxy: str | None) -> tuple[bool, dict]:
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS)
    opener = None
    if proxy:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    try:
        start = time.time()
        resp = (opener.open(req, timeout=timeout) if opener else urllib.request.urlopen(req, timeout=timeout))
        elapsed = round((time.time() - start) * 1000)
        return True, {
            "status": getattr(resp, "status", 200),
            "finalUrl": resp.geturl(),
            "elapsedMs": elapsed,
        }
    except urllib.error.HTTPError as e:
        return False, {"status": e.code, "error": str(e)}
    except Exception as e:
        return False, {"status": None, "error": str(e)}


def check_connectivity(url: str, profile_path: str | None = None, task_dir: str | None = None) -> dict:
    profile = _load_json(profile_path) if profile_path else {}
    cfg = _profile_connectivity(profile)
    timeout = int(cfg.get("timeoutSeconds", 12))
    retries = int(cfg.get("retries", 2))
    backoff_ms = int(cfg.get("backoffMs", 800))

    attempts = []
    selected = None
    for candidate in _candidate_urls(url, profile):
        for retry in range(retries + 1):
            ok, info = _open(candidate["url"], timeout=timeout, proxy=candidate.get("proxy"))
            attempt = {
                **candidate,
                "retry": retry,
                **info,
                "ok": ok,
            }
            attempts.append(attempt)
            if ok and info.get("status") and int(info.get("status")) < 400:
                selected = attempt
                break
            if retry < retries:
                time.sleep(backoff_ms / 1000.0)
        if selected:
            break

    result = {
        "ok": selected is not None,
        "inputUrl": url,
        "selected": selected,
        "attempts": attempts,
        "recommendation": {
            "mode": selected.get("mode") if selected else "manual-review",
            "reason": "Connectivity established" if selected else "All connectivity attempts failed; inspect network/proxy/mirror settings.",
        },
    }

    if task_dir:
        td = Path(task_dir)
        td.mkdir(parents=True, exist_ok=True)
        _save_json(str(td / "connectivity_report.json"), result)
    return result


def main(argv: list[str]) -> int:
    if len(argv) not in (2, 3, 4):
        print("Usage: site_connectivity_adapter.py <url> [profile.json] [task_dir]", file=sys.stderr)
        return 1
    url = argv[1]
    profile_path = argv[2] if len(argv) >= 3 else None
    task_dir = argv[3] if len(argv) == 4 else None
    print(json.dumps(check_connectivity(url, profile_path, task_dir), ensure_ascii=False, indent=2))
    return 0
