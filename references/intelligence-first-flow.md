# Intelligence-First Flow

Use this when onboarding a new or unfamiliar site.

## Flow
1. Initialize orchestrator with intelligence-first enabled.
2. Open the start URL.
3. Capture a bootstrap snapshot.
4. Run:
   - `intelligence_bootstrap.py <task_dir> <snapshot.txt> <base_url>`
5. This generates:
   - `<snapshot>.intel.json`
   - `<snapshot>.profile.json`
   - orchestrator intelligence metadata
6. Continue with the list/detail workflow using the intelligence output as guidance.

## Why this matters
This makes the platform smarter on first contact with a site:
- better route selection
- safer checkpoint detection
- faster profile bootstrapping
