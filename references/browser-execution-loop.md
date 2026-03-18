# Browser Execution Loop

Use this when route=`browser` or `hybrid`.

## Goal
Turn `browser_plan.json` into a real run with saved state and extracted results.

## Loop
1. Initialize runtime:
   - `browser_state_driver.py init <plan.json> <task_dir>`
2. Open the target URL with OpenClaw `browser.open` or `browser.navigate`.
3. Capture a snapshot with `browser.snapshot`.
4. Save snapshot text to a file in the task dir.
5. Parse it with `browser_extract_from_snapshot.py`.
6. Record extracted items with:
   - `browser_state_driver.py record <task_dir> <url> <items_json> <note>`
7. If pagination exists:
   - click next
   - repeat snapshot → parse → record
8. On failure:
   - save screenshot
   - `browser_state_driver.py fail <task_dir> <url> <reason>`
9. On completion:
   - `browser_state_driver.py complete <task_dir>`

## Human checkpoint rule
If login/MFA/captcha/approval is encountered:
- stop automated progression
- save screenshot and current URL
- report required human action
- resume only after human intervention

## Why this matters
This separates:
- browser action control (OpenClaw tool)
- deterministic runtime state
- extracted data persistence
- failure recovery hooks
