# Runbook Mode

Use runbook mode when you want the platform to emit a concrete operator/agent playbook for the next slice of work.

## Purpose
Translate workflow state into a compact, explicit sequence of actions:
- browser actions
- file outputs
- follow-up script commands
- artifact recording commands

## Script
- `browser_runbook_builder.py <task_dir>`

## Output
- `runbook.json`

## Why it matters
Runbook mode makes the platform feel like a product, not a pile of scripts:
- easier handoff
- easier debugging
- easier replay
- easier future automation
