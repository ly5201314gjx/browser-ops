# Browser Ops Strategy

## Route selection

### Route A — HTTP/API first
Use when:
- target data is directly accessible via HTML or JSON
- page is SSR or static
- browser is not needed for interaction

Pros:
- faster
- cheaper
- easier to recover

### Route B — Browser DOM route
Use when:
- page is SPA
- content is lazy-loaded
- interaction is needed (click, type, expand, infinite scroll)

Pros:
- can observe real rendered page state
- works for many modern UIs

### Route C — Hybrid route
Use when:
- browser can reveal network/API patterns
- browser is only needed to bootstrap tokens or inspect requests
- bulk extraction should happen outside browser after discovery

Pros:
- high scale once discovery is done
- more robust than pure click automation

### Route D — Human-in-the-loop
Use when:
- login requires user action
- MFA/captcha/approval wall appears
- site requires explicit user confirmation

Pros:
- compliant
- robust for protected workflows

## Failure recovery ladder

1. retry same step with bounded timeout
2. re-snapshot page and re-resolve element refs
3. use fallback selectors
4. refresh or reopen page
5. switch route (browser → hybrid or browser → human-in-loop)
6. persist failure artifacts and stop cleanly

## Observability defaults

For non-trivial tasks, capture:
- run log
- current URL
- screenshot on failure
- structured state/checkpoint
- extracted item count
- failed URL list

## Anti-fragility rules

- never rely on a single selector if a fallback is obvious
- prefer stable anchors: role/name, aria refs, semantic text, embedded JSON
- treat page network responses as first-class extraction sources
- when repeating on one site, convert discoveries into a reusable profile
