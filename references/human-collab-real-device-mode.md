# Human-Collab Real-Device Mode

This mode is for human-assisted browser work with a more realistic, device-aware interaction plan.

## Goals
- keep browser actions observable and stepwise
- use a device profile (desktop/mobile/tablet)
- pause at protected checkpoints instead of forcing through them
- produce a handoff packet when human intervention is required

## Scripts
- `device_profile_manager.py <task_dir> <profile_name>`
- `browser_human_mode.py enable <task_dir> [mode] [realism]`
- `browser_human_mode.py plan <task_dir>`
- `handoff_packet.py build <task_dir> [reason] [current_url] [screenshot_path] [snapshot_path]`
- `handoff_packet.py resume <task_dir> [note]`

## Recommended profiles
- `desktop-default`
- `mobile-default`
- `tablet-default`

## Boundary
This mode simulates a more realistic device posture and stepwise interaction style, but it does not attempt to bypass access controls, captcha, MFA, or other platform protections.
