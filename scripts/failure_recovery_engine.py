#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

from state_store import load_json, save_json


def _now() -> datetime:
    return datetime.now()


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _load_state(td: Path) -> dict:
    return load_json(str(td / "recovery_state.json"), default={
        "incidents": [],
        "openCount": 0,
        "resolvedCount": 0,
        "lastPlan": None,
    })


def _save_state(td: Path, state: dict) -> None:
    state["openCount"] = sum(1 for x in state.get("incidents", []) if x.get("status") == "open")
    state["resolvedCount"] = sum(1 for x in state.get("incidents", []) if x.get("status") == "resolved")
    save_json(str(td / "recovery_state.json"), state)


def classify_failure(stage: str, reason: str) -> str:
    r = (reason or "").lower()
    s = (stage or "").lower()
    if "browser boundary" in r or "interrupted browser slice" in r:
        return "browser-boundary-interruption"
    if "snapshot" in r or "artifact" in r or "missing" in r:
        return "missing-artifact"
    if "parser" in r or "extract" in r:
        return "parser-failure"
    if "route" in r:
        return "route-mismatch"
    if "detail" in s or "detail" in r:
        return "detail-batch-failure"
    if "report" in s or "report" in r:
        return "report-generation-failure"
    return "unknown-failure"


def register_failure(task_dir: str, stage: str, reason: str, url: str = "", snapshot_path: str = "", screenshot_path: str = "", retryable: bool = True) -> dict:
    td = Path(task_dir)
    state = _load_state(td)
    category = classify_failure(stage, reason)
    retry_budget_map = {
        "browser-boundary-interruption": 3,
        "missing-artifact": 2,
        "parser-failure": 2,
        "route-mismatch": 1,
        "detail-batch-failure": 2,
        "report-generation-failure": 2,
        "unknown-failure": 1,
    }
    cooldown_map = {
        "browser-boundary-interruption": 15,
        "missing-artifact": 20,
        "parser-failure": 30,
        "route-mismatch": 60,
        "detail-batch-failure": 30,
        "report-generation-failure": 20,
        "unknown-failure": 45,
    }
    incident = {
        "id": f"inc-{_now().strftime('%Y%m%d%H%M%S%f')}",
        "ts": _iso(_now()),
        "status": "open",
        "stage": stage,
        "reason": reason,
        "category": category,
        "url": url,
        "snapshotPath": snapshot_path,
        "screenshotPath": screenshot_path,
        "retryable": retryable,
        "retryCount": 0,
        "retryBudget": retry_budget_map.get(category, 1),
        "cooldownSeconds": cooldown_map.get(category, 45),
        "nextRetryAfter": _iso(_now()),
    }
    state.setdefault("incidents", []).append(incident)
    _save_state(td, state)
    return incident


def _retry_allowed(incident: dict) -> tuple[bool, str]:
    if not incident.get("retryable", True):
        return False, "Incident is marked non-retryable."
    if incident.get("retryCount", 0) >= incident.get("retryBudget", 1):
        return False, "Retry budget exhausted."
    next_retry_after = incident.get("nextRetryAfter")
    if next_retry_after:
        try:
            ready_at = datetime.fromisoformat(next_retry_after)
            if _now() < ready_at:
                return False, f"Cooldown active until {next_retry_after}."
        except ValueError:
            pass
    return True, "Retry allowed."


def _auto_resume_hooks(td: Path, orch: dict, runtime: dict, batch: dict, exec_report: dict, incidents: list[dict]) -> list[dict]:
    hooks = []
    pending = exec_report.get("pendingBrowserSteps", [])
    blocked = exec_report.get("blockedAfterBrowser", [])

    for incident in incidents:
        category = incident.get("category")
        snapshot_path = incident.get("snapshotPath")
        if category in {"browser-boundary-interruption", "missing-artifact"}:
            if snapshot_path and Path(snapshot_path).exists():
                hooks.append({
                    "kind": "auto-resolve-incident",
                    "priority": 1,
                    "incidentId": incident.get("id"),
                    "reason": "Required snapshot/artifact is now present; incident can be resolved.",
                })
        if category == "detail-batch-failure":
            idx = batch.get("currentIndex", 0)
            if idx < len(batch.get("items", [])):
                hooks.append({
                    "kind": "resume-detail-index",
                    "priority": 3,
                    "reason": f"Resume detail workflow from currentIndex={idx}.",
                    "index": idx,
                    "url": batch.get("items", [])[idx].get("link", ""),
                })

    if exec_report.get("stoppedAtBrowserBoundary") and pending:
        hooks.append({
            "kind": "resume-browser-slice",
            "priority": 1,
            "reason": "Browser boundary reached; complete pending browser steps before resuming blocked exec steps.",
            "pendingBrowserSteps": len(pending),
            "blockedAfterBrowser": len(blocked),
        })
    return hooks


def build_recovery_plan(task_dir: str) -> dict:
    td = Path(task_dir)
    orch = load_json(str(td / "orchestrator_state.json"), default={})
    runtime = load_json(str(td / "browser_runtime.json"), default={})
    batch = load_json(str(td / "detail_batch_state.json"), default={})
    exec_report = load_json(str(td / "runbook.exec.json"), default={})
    state = _load_state(td)
    open_incidents = [x for x in state.get("incidents", []) if x.get("status") == "open"]
    phase = orch.get("currentPhase", "list")

    actions = []
    actions.extend(_auto_resume_hooks(td, orch, runtime, batch, exec_report, open_incidents))

    if open_incidents:
        latest = open_incidents[-1]
        allowed, retry_note = _retry_allowed(latest)
        if allowed:
            actions.append({
                "kind": "retry-last-failed-slice",
                "priority": 2,
                "reason": f"Retryable open incident at stage {latest.get('stage')}. {retry_note}",
                "incidentId": latest.get("id"),
                "category": latest.get("category"),
            })
        else:
            actions.append({
                "kind": "human-review",
                "priority": 2,
                "reason": f"Incident at stage {latest.get('stage')} requires review. {retry_note}",
                "incidentId": latest.get("id"),
                "category": latest.get("category"),
            })

    if phase == "detail" and batch:
        idx = batch.get("currentIndex", 0)
        items = batch.get("items", [])
        if idx < len(items):
            actions.append({
                "kind": "resume-detail-index",
                "priority": 3,
                "reason": f"Resume detail workflow from currentIndex={idx}.",
                "index": idx,
                "url": items[idx].get("link", ""),
            })

    if phase == "list":
        visited = runtime.get("pagesVisited", 0)
        next_url = runtime.get("suggestedNextUrl") or orch.get("startUrl", "")
        actions.append({
            "kind": "resume-list-phase",
            "priority": 4,
            "reason": f"Resume list phase after pagesVisited={visited}.",
            "url": next_url,
        })

    if phase == "report":
        actions.append({
            "kind": "rebuild-report",
            "priority": 5,
            "reason": "Workflow is at report phase; rebuild final report.",
        })

    plan = {
        "createdAt": _iso(_now()),
        "taskDir": str(td),
        "phase": phase,
        "openIncidents": open_incidents,
        "recommendedActions": sorted(actions, key=lambda x: x.get("priority", 999)),
    }
    state["lastPlan"] = plan
    _save_state(td, state)
    save_json(str(td / "recovery_plan.json"), plan)
    return plan


def resolve_incident(task_dir: str, incident_id: str, note: str = "resolved") -> dict:
    td = Path(task_dir)
    state = _load_state(td)
    for incident in state.get("incidents", []):
        if incident.get("id") == incident_id:
            incident["status"] = "resolved"
            incident["resolvedAt"] = _iso(_now())
            incident["resolutionNote"] = note
            break
    _save_state(td, state)
    return state


def bump_retry(task_dir: str, incident_id: str) -> dict:
    td = Path(task_dir)
    state = _load_state(td)
    for incident in state.get("incidents", []):
        if incident.get("id") == incident_id:
            incident["retryCount"] = incident.get("retryCount", 0) + 1
            cooldown = incident.get("cooldownSeconds", 45)
            incident["nextRetryAfter"] = _iso(_now() + timedelta(seconds=cooldown))
            break
    _save_state(td, state)
    return state


def status(task_dir: str) -> dict:
    td = Path(task_dir)
    state = _load_state(td)
    return {
        "ok": True,
        "taskDir": str(td),
        "openCount": state.get("openCount", 0),
        "resolvedCount": state.get("resolvedCount", 0),
        "lastPlan": state.get("lastPlan"),
        "incidents": state.get("incidents", []),
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: failure_recovery_engine.py <register|plan|resolve|bump-retry|status> <task_dir> [...]", file=sys.stderr)
        raise SystemExit(1)
    cmd = sys.argv[1]
    if cmd == "register":
        stage = sys.argv[3] if len(sys.argv) > 3 else "unknown"
        reason = sys.argv[4] if len(sys.argv) > 4 else "unknown"
        url = sys.argv[5] if len(sys.argv) > 5 else ""
        snapshot = sys.argv[6] if len(sys.argv) > 6 else ""
        screenshot = sys.argv[7] if len(sys.argv) > 7 else ""
        retryable = (sys.argv[8].lower() != "false") if len(sys.argv) > 8 else True
        print(json.dumps(register_failure(sys.argv[2], stage, reason, url, snapshot, screenshot, retryable), ensure_ascii=False, indent=2))
    elif cmd == "plan":
        print(json.dumps(build_recovery_plan(sys.argv[2]), ensure_ascii=False, indent=2))
    elif cmd == "resolve":
        incident_id = sys.argv[3]
        note = sys.argv[4] if len(sys.argv) > 4 else "resolved"
        print(json.dumps(resolve_incident(sys.argv[2], incident_id, note), ensure_ascii=False, indent=2))
    elif cmd == "bump-retry":
        incident_id = sys.argv[3]
        print(json.dumps(bump_retry(sys.argv[2], incident_id), ensure_ascii=False, indent=2))
    elif cmd == "status":
        print(json.dumps(status(sys.argv[2]), ensure_ascii=False, indent=2))
    else:
        raise SystemExit(f"unknown command: {cmd}")
