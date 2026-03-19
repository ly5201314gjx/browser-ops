# Site Intelligence

Use site intelligence before or during a new-site workflow.

## Purpose
Deeply inspect a snapshot and answer:
- what kind of page is this?
- what route should be used?
- are there human checkpoints?
- is pagination likely present?
- what candidate links/structures are visible?

## Scripts
- `site_intelligence.py <snapshot.txt> <base_url>`
- `profile_suggester.py <snapshot.intel.json>`

## Outputs
- `<snapshot>.intel.json`
- `<snapshot>.profile.json`

## What it enables
- smarter route selection
- safer detection of login/captcha/MFA walls
- better profile bootstrapping for new sites
- faster onboarding of unfamiliar pages

## Boundary
This is deep inspection, not bypass tooling.
It identifies protected checkpoints and recommends human-in-the-loop where appropriate.
