#!/usr/bin/env python3
import json
from pathlib import Path


def _load(path: Path):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def build_report(task_dir: str) -> str:
    p = Path(task_dir)
    state = _load(p / "browser_runtime.json") or _load(p / "state.json")

    lines = [
        f"# Browser Ops Report",
        "",
        f"- Task dir: {p}",
        f"- Route: {state.get('route', '')}",
        f"- Status: {state.get('status', '')}",
        f"- Pages visited: {state.get('pagesVisited', 0)}",
        f"- List items extracted: {state.get('itemsExtracted', 0)}",
        f"- Detail pages extracted: {state.get('detailsExtracted', 0)}",
        f"- Failed URLs: {len(state.get('failedUrls', []))}",
        "",
    ]
    report = "\n".join(lines)
    (p / "report.md").write_text(report, encoding="utf-8")
    return report


if __name__ == "__main__":
    import sys
    print(build_report(sys.argv[1]))
