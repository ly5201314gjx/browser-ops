#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse

from browser_ops.core.state_store import load_json, save_json


def _read_text(path: str) -> str:
    p = Path(path)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def analyze_page_structure(snapshot_text: str) -> dict:
    lines = snapshot_text.splitlines()
    headings = [x.strip() for x in lines if 'heading "' in x.lower()][:20]
    links = [x.strip() for x in lines if 'link "' in x.lower()][:80]
    inputs = [x.strip() for x in lines if 'textbox' in x.lower() or 'searchbox' in x.lower() or 'password' in x.lower()][:40]
    buttons = [x.strip() for x in lines if 'button' in x.lower()][:60]
    iframe = 'iframe' in snapshot_text.lower()
    modal_like = any(k in snapshot_text.lower() for k in ['dialog', 'modal', 'drawer'])
    return {
        "headingCount": len(headings),
        "linkCount": len(links),
        "inputCount": len(inputs),
        "buttonCount": len(buttons),
        "hasIframe": iframe,
        "hasModalLikeUi": modal_like,
        "interactiveRegions": {
            "forms": len(inputs) > 0,
            "navigation": len(links) > 5,
            "actions": len(buttons) > 0,
        },
    }


def analyze_data_flow(snapshot_text: str, js_findings: dict, task_dir: Path) -> dict:
    keys = []
    for key in ["localStorage", "sessionStorage", "indexedDB", "cache", "history"]:
        if key.lower() in json.dumps(js_findings, ensure_ascii=False).lower() or key.lower() in snapshot_text.lower():
            keys.append(key)
    runtime = load_json(str(task_dir / "browser_runtime.json"), default={})
    return {
        "clientStorageSignals": keys,
        "hasSearchFlow": 'search' in snapshot_text.lower(),
        "hasPaginationSignal": 'next' in snapshot_text.lower() or 'pagination' in snapshot_text.lower(),
        "observedRuntimeKeys": sorted(runtime.keys())[:30],
    }


def analyze_network_dependencies(js_findings: dict, intel: dict) -> dict:
    raw = json.dumps(js_findings, ensure_ascii=False)
    urls = sorted(set(re.findall(r'https?://[^\s"\']+', raw)))[:80]
    api_like = sorted(set(re.findall(r'/api/[^\s"\']+', raw)))[:80]
    host = urlparse(intel.get('baseUrl', '')).netloc
    first_party = [u for u in urls if host and host in u]
    third_party = [u for u in urls if u not in first_party]
    return {
        "firstPartyApis": first_party[:30],
        "thirdPartyApis": third_party[:50],
        "apiLikePaths": api_like,
        "dependencyCount": len(urls) + len(api_like),
    }


def analyze_state_machine(snapshot_text: str, interaction_findings: dict, intel: dict) -> dict:
    blob = snapshot_text.lower() + "\n" + json.dumps(interaction_findings, ensure_ascii=False).lower()
    states = []
    for name, needles in {
        'empty': ['暂无', 'empty', '没有保存', 'no results'],
        'loading': ['加载', 'loading', '生成中', '正在'],
        'error': ['失败', 'error', '拦截', '重试'],
        'success': ['success', '完成', '已保存'],
        'login': ['登录', 'sign in', 'password'],
    }.items():
        if any(n in blob for n in needles):
            states.append(name)
    return {
        "states": states,
        "blockingStates": [s for s in states if s in {'error', 'login'}],
        "recommendedRoute": intel.get('recommendedRoute', ''),
    }


def analyze_interaction_complexity(snapshot_text: str, intel: dict, interaction_findings: dict) -> dict:
    score = 1
    lower = snapshot_text.lower()
    if 'iframe' in lower:
        score += 1
    if any(k in lower for k in ['dialog', 'modal', 'drawer']):
        score += 1
    if any(k in lower for k in ['drag', 'canvas', 'webrtc', 'map']):
        score += 1
    if intel.get('recommendedRoute') in {'hybrid', 'human'}:
        score += 1
    if interaction_findings:
        score += 1
    return {
        "complexityScore": min(score, 5),
        "recommendedMode": intel.get('recommendedRoute', 'browser'),
    }


def analyze_security_barriers(snapshot_text: str, intel: dict, interaction_findings: dict) -> dict:
    checkpoints = intel.get('humanCheckpoints', {})
    blob = snapshot_text.lower() + json.dumps(interaction_findings, ensure_ascii=False).lower()
    anti = []
    for x in ['captcha', 'cloudflare', 'mfa', 'approval', 'cors', 'cross-origin', '拦截']:
        if x in blob:
            anti.append(x)
    return {
        "loginWall": checkpoints.get('login', False),
        "captcha": checkpoints.get('captcha', False) or 'captcha' in anti,
        "mfa": checkpoints.get('mfa', False) or 'mfa' in anti,
        "approvalGate": checkpoints.get('approval', False) or 'approval' in anti,
        "antiAutomationSignals": anti,
    }


def analyze_extractability(snapshot_text: str, intel: dict, js_findings: dict) -> dict:
    link_count = snapshot_text.lower().count('link "')
    repeated = link_count >= 8
    return {
        "estimatedStructureStability": 'medium' if repeated else 'low',
        "hasRepeatedItems": repeated,
        "profileCandidate": True,
        "recommendedFields": ['title', 'link', 'summary', 'content'],
        "suggestedRoute": intel.get('recommendedRoute', 'browser'),
    }


def analyze_product_intent(snapshot_text: str, base_url: str) -> dict:
    lower = snapshot_text.lower()
    ctas = []
    for x in ['搜索', '登录', '注册', 'create account', '生成', '上传', 'download', 'share', '收藏']:
        if x.lower() in lower:
            ctas.append(x)
    product_guess = 'content or tool site'
    if 'create account' in lower or 'sign in' in lower:
        product_guess = 'account-based web application'
    elif '生成' in lower or 'prompt' in lower:
        product_guess = 'ai utility application'
    elif 'upload' in lower or 'share' in lower:
        product_guess = 'file sharing tool'
    return {
        "baseUrl": base_url,
        "primaryCTA": ctas[:10],
        "productGuess": product_guess,
        "coreIntent": ctas[0] if ctas else 'unknown',
    }


def build_summary(dimensions: dict, intel: dict) -> dict:
    complexity = dimensions['interaction_complexity']['complexityScore']
    barriers = len(dimensions['security_barriers']['antiAutomationSignals'])
    extractable = 4 if dimensions['extractability']['profileCandidate'] else 2
    return {
        "siteType": dimensions['product_intent']['productGuess'],
        "recommendedRoute": intel.get('recommendedRoute', 'browser'),
        "automationDifficulty": min(5, complexity + (1 if barriers else 0)),
        "extractionValue": extractable,
    }


def analyze(task_dir: str, url: str, snapshot_path: str) -> dict:
    td = Path(task_dir)
    snapshot_text = _read_text(snapshot_path)
    intel = load_json(str(Path(snapshot_path).with_suffix('.intel.json')), default={})
    if not intel:
        intel = load_json(str(td / 'intelligence.json'), default={})
    js_findings = load_json(str(td / 'artifacts' / 'js_findings.json'), default={})
    interaction_findings = load_json(str(td / 'artifacts' / 'interaction_findings.json'), default={})

    dimensions = {
        'page_structure': analyze_page_structure(snapshot_text),
        'data_flow': analyze_data_flow(snapshot_text, js_findings, td),
        'network_dependencies': analyze_network_dependencies(js_findings, {'baseUrl': url, **intel}),
        'state_machine': analyze_state_machine(snapshot_text, interaction_findings, intel),
        'interaction_complexity': analyze_interaction_complexity(snapshot_text, intel, interaction_findings),
        'security_barriers': analyze_security_barriers(snapshot_text, intel, interaction_findings),
        'extractability': analyze_extractability(snapshot_text, intel, js_findings),
        'product_intent': analyze_product_intent(snapshot_text, url),
    }

    result = {
        'target': url,
        'summary': build_summary(dimensions, intel),
        'dimensions': dimensions,
        'finalJudgement': {
            'bestResearchMode': intel.get('recommendedRoute', 'browser'),
            'bestAutomationMode': intel.get('recommendedRoute', 'browser'),
            'humanCheckpointNeeded': dimensions['security_barriers']['loginWall'] or dimensions['security_barriers']['captcha'] or dimensions['security_barriers']['mfa'],
            'profileCandidate': dimensions['extractability']['profileCandidate'],
        }
    }
    save_json(str(td / 'deep_analysis.json'), result)
    return result


def main(argv: list[str]) -> int:
    import sys

    if len(argv) != 4:
        print('Usage: deep_analysis_engine.py <task_dir> <url> <snapshot.txt>', file=sys.stderr)
        return 1
    result = analyze(argv[1], argv[2], argv[3])
    print(json.dumps({'ok': True, 'output': str(Path(argv[1]) / 'deep_analysis.json'), 'recommendedRoute': result['summary']['recommendedRoute']}, ensure_ascii=False))
    return 0
