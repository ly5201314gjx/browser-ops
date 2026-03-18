# Consent-Aware Interaction Policy

This module rewrites a user-provided consent prompt into a more natural, device-aware interaction description while preserving the original meaning and compliance boundary.

## Goals
- preserve original consent meaning and compliance statements
- make the prompt read closer to real mobile/tablet/desktop interaction rhythms
- attach parameter guidance for pause timing, touch rhythm, swipe motion, and bounded randomization
- avoid any bypass, evasion, or attack-oriented instruction

## Scripts
- `interaction_policy_engine.py <task_dir> [device_profile]`
- `consent_prompt_rewriter.py <task_dir> <input_txt> [device_profile]`

## Outputs
- `interaction_policy.json`
- `consent_prompt_rewrite.json`

## Boundaries
This module does not generate executable scripts, bypass logic, evasion instructions, or risk-control defeat strategies. It is only for compliant wording refinement and parameter explanation.
