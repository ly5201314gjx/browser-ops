# Real Browser Demo

This proves the browser route with the real OpenClaw `browser` tool.

## Demo flow
1. Build a browser plan:
   - `browser_plan_builder.py <profile.json> <task_dir>`
2. Initialize runtime:
   - `browser_state_driver.py init <task_dir>/browser_plan.json <task_dir>`
3. Open the page with OpenClaw `browser.open`.
4. Capture a real snapshot with `browser.snapshot`.
5. Save snapshot text to `<task_dir>/snapshot.txt`.
6. Parse snapshot:
   - `browser_extract_from_snapshot.py <task_dir>/snapshot.txt`
7. Record progress:
   - `browser_state_driver.py record <task_dir> <url> <task_dir>/snapshot.items.json "real browser snapshot parsed"`
8. Complete:
   - `browser_state_driver.py complete <task_dir>`
9. Build a report:
   - `report_builder.py <task_dir>`

## What this proves
- OpenClaw browser tool can feed the skill runtime
- snapshot text can be persisted and parsed into items
- browser route can maintain state and produce results without ad-hoc manual bookkeeping

## Next upgrade targets
- auto-save browser snapshots and screenshots from orchestration code
- paginate with real clicks and repeated snapshot parsing
- selector-driven extraction from snapshot or DOM metadata
- failure screenshots + checkpoint resume
