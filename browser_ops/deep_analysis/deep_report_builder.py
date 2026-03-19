#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from browser_ops.core.state_store import load_json


def build_report(task_dir: str) -> str:
    td = Path(task_dir)
    data = load_json(str(td / 'deep_analysis.json'), default={})
    dims = data.get('dimensions', {})
    summary = data.get('summary', {})
    final = data.get('finalJudgement', {})

    lines = [
        '# Deep Analysis Report',
        '',
        f"- Target: {data.get('target', '')}",
        f"- Site type: {summary.get('siteType', '')}",
        f"- Recommended route: {summary.get('recommendedRoute', '')}",
        f"- Automation difficulty: {summary.get('automationDifficulty', '')}/5",
        f"- Extraction value: {summary.get('extractionValue', '')}/5",
        '',
        '## 8 Dimensions',
        '',
        f"### 1. Page Structure\n- {dims.get('page_structure', {})}",
        '',
        f"### 2. Data Flow\n- {dims.get('data_flow', {})}",
        '',
        f"### 3. Network Dependencies\n- {dims.get('network_dependencies', {})}",
        '',
        f"### 4. State Machine\n- {dims.get('state_machine', {})}",
        '',
        f"### 5. Interaction Complexity\n- {dims.get('interaction_complexity', {})}",
        '',
        f"### 6. Security Barriers\n- {dims.get('security_barriers', {})}",
        '',
        f"### 7. Extractability\n- {dims.get('extractability', {})}",
        '',
        f"### 8. Product Intent\n- {dims.get('product_intent', {})}",
        '',
        '## Final Judgement',
        '',
        f"- Best research mode: {final.get('bestResearchMode', '')}",
        f"- Best automation mode: {final.get('bestAutomationMode', '')}",
        f"- Human checkpoint needed: {final.get('humanCheckpointNeeded', False)}",
        f"- Profile candidate: {final.get('profileCandidate', False)}",
    ]
    out = '\n'.join(lines)
    (td / 'deep_report.md').write_text(out, encoding='utf-8')
    return out


def main(argv: list[str]) -> int:
    import sys

    if len(argv) != 2:
        print('Usage: deep_report_builder.py <task_dir>', file=sys.stderr)
        return 1
    print(build_report(argv[1]))
    return 0
