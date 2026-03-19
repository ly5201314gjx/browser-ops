#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from browser_ops.core.state_store import load_json, save_json


def bootstrap(task_dir: str, snapshot_path: str, base_url: str) -> dict:
    import sys

    td = Path(task_dir).resolve()
    base = Path(__file__).resolve().parent.parent.parent / 'scripts'
    intel_script = base / 'site_intelligence.py'
    profile_script = base / 'profile_suggester.py'
    deep_script = base / 'deep_analysis_engine.py'
    deep_report_script = base / 'deep_report_builder.py'

    intel_proc = subprocess.run(
        [sys.executable, str(intel_script), snapshot_path, base_url],
        capture_output=True,
        text=True,
    )
    if intel_proc.returncode != 0:
        raise SystemExit(intel_proc.stderr or intel_proc.stdout)

    intel_out = Path(snapshot_path).with_suffix('.intel.json')
    profile_proc = subprocess.run(
        [sys.executable, str(profile_script), str(intel_out)],
        capture_output=True,
        text=True,
    )
    if profile_proc.returncode != 0:
        raise SystemExit(profile_proc.stderr or profile_proc.stdout)

    deep_proc = subprocess.run(
        [sys.executable, str(deep_script), str(td), base_url, snapshot_path],
        capture_output=True,
        text=True,
    )
    if deep_proc.returncode != 0:
        raise SystemExit(deep_proc.stderr or deep_proc.stdout)

    deep_report_proc = subprocess.run(
        [sys.executable, str(deep_report_script), str(td)],
        capture_output=True,
        text=True,
    )
    if deep_report_proc.returncode != 0:
        raise SystemExit(deep_report_proc.stderr or deep_report_proc.stdout)

    intel_data = load_json(str(intel_out), default={})
    profile_out = intel_out.with_suffix('.profile.json')
    profile_data = load_json(str(profile_out), default={})
    deep_data = load_json(str(td / 'deep_analysis.json'), default={})

    orchestrator = load_json(str(td / 'orchestrator_state.json'), default={})
    orchestrator['intelligence'] = {
        'snapshotPath': str(Path(snapshot_path).resolve()),
        'intelPath': str(intel_out.resolve()),
        'profileDraftPath': str(profile_out.resolve()),
        'deepAnalysisPath': str((td / 'deep_analysis.json').resolve()),
        'deepReportPath': str((td / 'deep_report.md').resolve()),
        'pageType': intel_data.get('pageType'),
        'recommendedRoute': intel_data.get('recommendedRoute'),
        'automationDifficulty': deep_data.get('summary', {}).get('automationDifficulty'),
        'extractionValue': deep_data.get('summary', {}).get('extractionValue'),
    }
    orchestrator.setdefault('notes', []).append({
        'kind': 'intelligence-bootstrap',
        'pageType': intel_data.get('pageType'),
        'recommendedRoute': intel_data.get('recommendedRoute'),
        'deepAnalysis': True,
    })
    save_json(str(td / 'orchestrator_state.json'), orchestrator)

    return {
        'ok': True,
        'intelPath': str(intel_out),
        'profileDraftPath': str(profile_out),
        'deepAnalysisPath': str(td / 'deep_analysis.json'),
        'deepReportPath': str(td / 'deep_report.md'),
        'pageType': intel_data.get('pageType'),
        'recommendedRoute': intel_data.get('recommendedRoute'),
        'profileName': profile_data.get('name'),
    }


def main(argv: list[str]) -> int:
    import sys

    if len(argv) != 4:
        print('Usage: intelligence_bootstrap.py <task_dir> <snapshot.txt> <base_url>', file=sys.stderr)
        return 1
    print(json.dumps(bootstrap(argv[1], argv[2], argv[3]), ensure_ascii=False))
    return 0
