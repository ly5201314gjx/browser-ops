# Autopilot Mode

Autopilot mode executes the non-browser portion of the next runbook slice automatically.

## Goal
Reduce manual glue work while keeping browser actions explicit and controllable.

## Scripts
- `runbook_executor.py <runbook.json> [cwd]`
- `autopilot_tick.py <task_dir>`

## Behavior
1. Build the latest runbook.
2. Execute all `exec` and `note` steps.
3. Stop before browser actions.
4. Emit which browser steps still need operator/agent control.

## Why this matters
This is the bridge from a strong semi-automatic system to a more product-like workflow engine.
