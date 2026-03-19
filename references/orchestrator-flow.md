# Orchestrator Flow

Use `browser_ops_orchestrator.py` as the top-level coordinator.

## Purpose
Coordinate the whole workflow instead of manually juggling individual scripts.

## Phases
1. `list`
   - open start page
   - snapshot
   - process page
   - follow pagination until page limit or no next page

2. `detail-queue`
   - build `detail_queue.json`
   - initialize `detail_batch_state.json`

3. `detail`
   - get next detail item
   - open detail URL
   - snapshot
   - process detail snapshot
   - mark done/fail
   - repeat

4. `report`
   - rebuild final report

## Commands
- `browser_ops_orchestrator.py init <profile.json> <task_dir> [detail_limit] [page_limit]`
- `browser_ops_orchestrator.py status <task_dir>`
- `browser_ops_orchestrator.py next <task_dir>`
- `browser_ops_orchestrator.py phase <task_dir> <phase>`
- `browser_ops_orchestrator.py note <task_dir> <note>`

## Design principle
The orchestrator does not replace browser tool control.
Instead, it tells the agent exactly what the next action is and keeps the overall workflow coherent.

This keeps the system:
- deterministic in state
- flexible in browser interaction
- recoverable after interruptions
