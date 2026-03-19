# Action Policy Layer

The action policy layer merges:
- site profile strategy fields
- device profile defaults
- human-collab mode policies
- bounded interaction timing/motion settings

## Scripts
- `action_policy_engine.py <task_dir> [profile.json]`
- `browser_plan_builder.py <profile.json> <task_dir>`
- `browser_runbook_builder.py <task_dir>`

## New profile fields
- `preferredDevice`
- `navigationStyle`
- `riskTolerance`
- `checkpointPolicy`
- `interactionPolicy`

## Result
Runbooks and browser plans can now carry action-policy metadata such as:
- device
- navigation style
- risk tolerance
- checkpoint policy
- timing pauses
- touch rhythm
- motion / scroll pause
- bounded randomization

## Boundary
This is for compliant interaction shaping and workflow consistency. It does not add evasion, bypass, or attack behavior.
