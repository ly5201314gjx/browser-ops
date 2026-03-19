# Failure Recovery System

The failure recovery system turns isolated failure logs into a resumable recovery workflow.

## Components
- `failure_recovery_engine.py`
- `recovery_runbook_builder.py`
- `failure_artifacts.json`
- `recovery_state.json`
- `recovery_plan.json`
- `recovery_runbook.json`

## Capabilities
- register failures as incidents
- classify incidents by recovery-relevant failure category
- track open/resolved incidents
- apply retry budgets and cooldown windows
- build a recovery plan from orchestrator/runtime/batch/exec state
- emit a recovery runbook
- connect autopilot failures into the recovery registry
- use auto-resume hooks when artifacts or browser-slice prerequisites become available

## Recovery action types
- `resume-browser-slice`
- `retry-last-failed-slice`
- `human-review`
- `resume-detail-index`
- `resume-list-phase`
- `rebuild-report`

## Boundary
Recovery focuses on safe resume, bounded retry, human review, and artifact-driven inspection. It does not bypass security controls.
