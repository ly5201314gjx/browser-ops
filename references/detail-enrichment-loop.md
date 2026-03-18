# Detail Enrichment Loop

Use this after list extraction when you need richer per-item content.

## Loop
1. Read candidate item links from `results.jsonl`.
2. Open one detail URL with the browser tool.
3. Capture a snapshot.
4. Save the snapshot to `<task_dir>/detail-N.txt`.
5. Process it with:
   - `browser_detail_processor.py <task_dir> <detail-N.txt> <detail_url> <source_item_link>`
6. Repeat for the next item until the desired count or limit is reached.
7. Rebuild the report.

## Outputs
- `detail_results.jsonl`
- `last_detail.json`
- updated `browser_runtime.json`

## Proven demo
Validated on a real Hacker News outbound article opened through OpenClaw browser, with title and paragraph content extracted into `detail_results.jsonl`.
