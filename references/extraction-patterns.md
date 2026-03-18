# Extraction Patterns

## Prefer these data sources in order
1. Embedded JSON in script tags or app bootstrap data
2. Stable API/XHR/GraphQL responses
3. Semantic DOM selectors (role/text/aria)
4. Generic CSS selectors
5. XPath as last resort

## Common patterns

### Embedded JSON
- Look for `__NEXT_DATA__`, `__NUXT__`, bootstrap state, hydration payloads.
- Prefer extracting structured objects before scraping rendered text.

### Semantic DOM
- Prefer stable anchors such as heading text, links, role names, buttons with labels.
- Use fallback selectors in profiles.

### Infinite scroll
- Scroll in bounded increments.
- Detect no-growth conditions.
- Stop when item count stops increasing for N cycles.

### Pagination
- Prefer explicit next-page links over guessed URL patterns.
- Record page index and next URL in state.

### Detail extraction
- Normalize whitespace.
- Save source URL.
- Keep raw fragments when field confidence is low.
