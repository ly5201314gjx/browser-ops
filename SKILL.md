---
name: 浏览器自研技能
description: Browser automation and web extraction platform for OpenClaw. Use when the user wants to automate websites, click/type/fill forms, capture screenshots, crawl list/detail pages, paginate, extract structured data, observe page/network behavior, or build reusable browser-driven workflows. Prefer for browser-based operations that need stronger execution, recovery, logging, checkpoints, site profiles, or mixed automation + crawling flows. Do not use to bypass captchas, evade access controls, or break platform security mechanisms; instead use human-in-the-loop checkpoints for login, MFA, captcha, or approval walls.
---

# Browser Ops

Build and run browser automation, crawling, deep site analysis, handoff, recovery, and autopilot workflows in a reusable, profile-driven, observable way.

## Current platform shape

Browser Ops is no longer just a browser automation skill. It is now an intelligence-driven browser operations platform with these major layers:

- `browser_ops/core` — shared state/profile helpers
- `browser_ops/orchestration` — route and workflow coordination
- `browser_ops/intelligence` — page classification + intelligence bootstrap
- `browser_ops/deep_analysis` — 8-dimensional deep site analysis
- `browser_ops/policy` — interaction/action policy generation
- `browser_ops/workflow` — plan, runbook, handoff, recovery-runbook builders
- `browser_ops/execution` — list/detail processors, queue/batch drivers, crawlers
- `browser_ops/control` — next-step, autopilot, state driver, human-mode, handoff packets
- `browser_ops/recovery` — incident tracking and recovery planning
- `browser_ops/support` — artifacts, device profiles, connectivity, reporting

## Core rules

- Prefer the cheapest viable strategy first: HTTP/API → browser DOM extraction → richer browser workflow.
- Do not build bypass tooling for captcha, MFA, login walls, or access-control mechanisms.
- When a workflow hits human verification or approval, pause and switch to human-in-the-loop.
- Always save structured outputs, progress state, and failure artifacts when the task is non-trivial.
- For repeatable site work, create or update a site profile instead of hardcoding one-off logic.
- If deep analysis indicates high friction or human-gated flow, prefer conservative policy and human review over stubborn retries.

## Core algorithm

Browser Ops now follows a decision chain closer to a real operations platform:

1. **Site Intelligence** → classify page / checkpoints / route
2. **Deep Analysis** → inspect 8 dimensions and score difficulty
3. **Action Policy** → tune timing / risk / checkpoint posture
4. **Runbook / Handoff / Recovery** → produce resumable operator workflow
5. **Autopilot / Next Step** → continue automatically when safe, pause for human when needed

Prefer this mental model when using the skill: first understand the site, then decide the route, then decide how aggressively to operate it.

## Deep Analysis (8 dimensions)

For deep-dive website research, the skill can now generate `deep_analysis.json` and `deep_report.md` using eight dimensions:

1. 页面结构（page structure）
2. 数据流（data flow）
3. 网络依赖（network dependencies）
4. 状态机（state machine）
5. 交互复杂度（interaction complexity）
6. 安全与拦截（security barriers）
7. 可提取性（extractability）
8. 产品意图（product intent）

This deep-analysis output already feeds into:
- intelligence bootstrap
- report builder
- runbook generation
- handoff packets
- recovery planning
- autopilot decisions
- next-step advice
- action policy tuning

Use deep analysis when the user wants to deeply inspect a site, understand how it works, compare automation routes, estimate difficulty, or produce a reusable site strategy.

## Strategy router

Select one route before execution:

1. **HTTP route**
   - Use when pages or APIs are directly fetchable.
   - Best for static pages, JSON APIs, RSS, SSR pages.

2. **Browser route**
   - Use when the page needs rendering, clicks, scrolls, or form interaction.
   - Best for SPA, lazy-loaded lists, modal/dialog flows.

3. **Hybrid route**
   - Use browser to discover page structure or API requests, then switch to HTTP for bulk extraction.
   - Best for modern apps where data lives in XHR/fetch or embedded JSON.

4. **Human-in-the-loop route**
   - Use when login, MFA, captcha, consent, or risk review blocks progress.
   - Advance as far as possible, snapshot the state, then ask the human to take over.

## Bundled resources

Read these references as needed:

- `references/strategy.md` — routing rules, failure recovery, and escalation logic.
- `references/site-profile-template.md` — how to describe a site in a reusable config.
- `references/workflow-recipes.md` — common automation/crawl patterns.
- `references/extraction-patterns.md` — ways to extract DOM/JSON/API content safely and robustly.
- `references/browser-execution-loop.md` — how to run browser/hybrid routes with snapshots, parsed items, runtime state, and completion/failure tracking.
- `references/real-browser-demo.md` — a proven demo path using the real OpenClaw browser tool.
- `references/pagination-loop.md` — how to run real multi-page browser extraction loops.
- `references/detail-enrichment-loop.md` — how to enrich list items by opening real detail pages and extracting structured content.
- `references/detail-batch-loop.md` — how to process multiple detail pages with a queue-driven workflow.
- `references/orchestrator-flow.md` — how to coordinate list, pagination, detail queue, detail batch, and report as one workflow.
- `references/artifacts-and-failures.md` — how to persist artifacts, failure evidence, and resumable run metadata.
- `references/runbook-mode.md` — how to emit product-like operator runbooks from workflow state.
- `references/demo-showcase.md` — public demo and clean-package guidance for a more showcase-ready skill.
- `references/site-intelligence.md` — deep inspection and profile-bootstrapping guidance for new sites.
- `references/deep-analysis.md` — how 8-dimensional deep analysis works and where it feeds into the system.
- `references/intelligence-first-flow.md` — how to run the orchestrator in intelligence-first mode for new sites.
- `references/autopilot-mode.md` — how to auto-execute non-browser runbook steps while keeping browser actions explicit.
- `references/device-profiles.md` — standard device profiles and interaction pacing for realistic browser workflows.
- `references/human-collab-real-device-mode.md` — human-assisted, device-aware workflow rules and handoff packet behavior.
- `references/consent-aware-interaction-policy.md` — compliant consent-prompt rewriting and bounded interaction-parameter guidance.
- `references/action-policy-layer.md` — how profile strategy, device posture, and human-mode policies merge into browser plans and runbooks.
- `references/browser-handoff-payload.md` — how to package browser-controlled next steps with action-policy context for handoff.
- `references/failure-recovery-system.md` — how incidents, recovery plans, and recovery runbooks work together.
- `references/safety-boundaries.md` — safety and legal boundary rules for browser ops.

## Deterministic scripts

Use these scripts for deterministic work:

- `scripts/run_browser_job.py` — run one browser job from a JSON config.
- `scripts/crawl_orchestrator.py` — run a profile-driven list/detail crawl with checkpoints and outputs.
- `scripts/http_crawler.py` — execute the HTTP route directly for list/detail extraction.
- `scripts/browser_plan_builder.py` — generate a browser action plan for browser/hybrid routes.
- `scripts/browser_state_driver.py` — maintain browser runtime state, recorded items, failures, and completion.
- `scripts/browser_extract_from_snapshot.py` — parse snapshot text into structured items as an MVP extraction bridge.
- `scripts/browser_page_processor.py` — process page snapshots into list items plus suggested next-page URLs.
- `scripts/browser_detail_processor.py` — process detail-page snapshots into structured enriched records.
- `scripts/detail_queue_builder.py` — build a detail extraction queue from list results.
- `scripts/detail_batch_driver.py` — drive queue-based multi-detail processing with success/failure accounting.
- `scripts/browser_ops_orchestrator.py` — top-level coordinator for list, pagination, detail queue, detail batch, and report phases.
- `scripts/browser_next_step.py` — emit the next precise operator/agent action from current workflow state.
- `scripts/browser_runbook_builder.py` — emit a concrete runbook.json for the next operator/agent slice.
- `scripts/runbook_executor.py` — execute non-browser runbook steps automatically and stop at browser-controlled actions.
- `scripts/autopilot_tick.py` — rebuild the current runbook and execute its non-browser portion as one autopilot tick.
- `scripts/site_intelligence.py` — deeply inspect a snapshot to classify page type, detect checkpoints, suggest route, and find pagination/link candidates.
- `scripts/profile_suggester.py` — turn site-intelligence output into a draft reusable site profile.
- `scripts/intelligence_bootstrap.py` — push site-intelligence + deep-analysis output into orchestrator state for intelligence-first onboarding.
- `scripts/device_profile_manager.py` — assign a consistent desktop/mobile/tablet device profile to the current task.
- `scripts/browser_human_mode.py` — enable human-assisted realistic interaction mode and generate an interaction plan.
- `scripts/interaction_policy_engine.py` — build bounded, device-aware interaction timing/motion policies for compliant browser workflows.
- `scripts/action_policy_engine.py` — merge site profile strategy, device profile, human mode, and deep-analysis posture into one action policy layer.
- `scripts/browser_handoff_payload.py` — package pending browser steps together with action-policy context for human/agent handoff.
- `scripts/consent_prompt_rewriter.py` — rewrite a user-provided consent prompt into a more natural device-aware version while preserving compliance boundaries.
- `scripts/failure_recovery_engine.py` — register incidents, track recovery state, and build recovery plans from workflow state + deep-analysis signals.
- `scripts/recovery_runbook_builder.py` — emit a recovery-focused runbook from current incidents and workflow state.
- `scripts/handoff_packet.py` — create/resume human handoff packets for blocked or protected workflow steps.
- `scripts/artifact_recorder.py` — persist artifact and failure evidence metadata for inspection and recovery.
- `scripts/report_builder.py` — build markdown summaries from run artifacts and include deep-analysis summaries.
- `scripts/deep_analysis_engine.py` — generate 8-dimensional deep-analysis output from a task snapshot.
- `scripts/deep_report_builder.py` — build a human-readable report from `deep_analysis.json`.

## Standard workflow

1. Clarify the task target:
   - site/app
   - operation type: automate / extract / crawl / mixed / deep research
   - login needed or not
   - expected output format

2. Choose a route using `references/strategy.md`.

3. If the site is new or strategically important, prefer intelligence-first mode and consider deep analysis early.

4. Run the job:
   - save outputs to a task folder
   - persist checkpoint state
   - save failure screenshots/logs when useful
   - emit deep-analysis artifacts when the task needs deeper understanding

5. Summarize results:
   - what worked
   - what failed
   - what needs human action
   - what deep analysis concluded
   - where artifacts were saved

## Output conventions

Prefer saving artifacts under a task-specific folder inside the workspace, for example:

- `logs/browser-ops/<task>/run.log`
- `logs/browser-ops/<task>/artifacts/`
- `logs/browser-ops/<task>/state.json`
- `logs/browser-ops/<task>/results.jsonl`
- `logs/browser-ops/<task>/deep_analysis.json`
- `logs/browser-ops/<task>/deep_report.md`
- `logs/browser-ops/<task>/report.md`

## For skill development

When extending this skill:
- keep SKILL.md lean
- move details into references
- prefer config-driven site support
- test scripts on a representative sample
- package only after the MVP works
