# Browser Handoff Payload

Browser handoff payloads package the next browser-controlled steps together with action-policy context.

## Scripts
- `browser_handoff_payload.py <task_dir>`
- `autopilot_tick.py <task_dir>`
- `handoff_packet.py build <task_dir> ...`

## Contents
- task phase
- effective route
- headline
- browser steps still pending
- action policy summary
- interaction timing / motion policy

## Why it matters
This makes browser work easier to hand off between:
- human-assisted execution
- agent-guided browser operation
- future semi-automatic browser runners

Autopilot should stop at the first browser boundary, preserve the pending browser steps, and mark downstream exec steps as blocked until the browser-controlled slice is completed.

## Boundary
This payload improves workflow clarity and action consistency. It does not add bypass, evasion, or attack behavior.
