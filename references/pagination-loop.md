# Pagination Loop

Use this when a browser route has a discoverable next page.

## Loop
1. Open page N with the browser tool.
2. Snapshot the page.
3. Save snapshot text to `<task_dir>/pageN.txt`.
4. Process it with:
   - `browser_page_processor.py <task_dir> <pageN.txt> <current_url> <note>`
5. Read `suggestedNextUrl` from `browser_runtime.json`.
6. If present and page limit not reached:
   - navigate to `suggestedNextUrl`
   - repeat
7. Complete runtime and build report.

## Notes
- `results.jsonl` may contain both `kind=item` and `kind=pagination` records.
- `itemsExtracted` counts only non-pagination items.
- Deduplication happens by `(kind, link)`.

## Proven demo
This loop has been validated on public Hacker News pages using the real OpenClaw browser tool and a two-page run.
