#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def _load(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {}


def build_report(task_dir: str) -> str:
    p = Path(task_dir)
    state = _load(p / 'browser_runtime.json') or _load(p / 'state.json')
    deep = _load(p / 'deep_analysis.json')

    lines = [
        '# Browser Ops Report',
        '',
        f'- Task dir: {p}',
        f"- Route: {state.get('route', '')}",
        f"- Status: {state.get('status', '')}",
        f"- Pages visited: {state.get('pagesVisited', 0)}",
        f"- List items extracted: {state.get('itemsExtracted', 0)}",
        f"- Detail pages extracted: {state.get('detailsExtracted', 0)}",
        f"- Failed URLs: {len(state.get('failedUrls', []))}",
        '',
    ]
    if deep:
        lines += [
            '## Deep Analysis Summary',
            '',
            f"- Site type: {deep.get('summary', {}).get('siteType', '')}",
            f"- Recommended route: {deep.get('summary', {}).get('recommendedRoute', '')}",
            f"- Automation difficulty: {deep.get('summary', {}).get('automationDifficulty', '')}/5",
            f"- Extraction value: {deep.get('summary', {}).get('extractionValue', '')}/5",
            f"- Human checkpoint needed: {deep.get('finalJudgement', {}).get('humanCheckpointNeeded', False)}",
            '',
            f"- Deep analysis file: {p / 'deep_analysis.json'}",
            f"- Deep report file: {p / 'deep_report.md'}",
            '',
        ]
    report = '\n'.join(lines)
    (p / 'report.md').write_text(report, encoding='utf-8')
    return report


def main(argv: list[str]) -> int:
    import sys

    if len(argv) != 2:
        print('Usage: report_builder.py <task_dir>', file=sys.stderr)
        return 1
    print(build_report(argv[1]))
    return 0
