# Detail Batch Loop

Use this to process multiple detail pages from list extraction outputs.

## Flow
1. Build detail queue:
   - `detail_queue_builder.py <task_dir> <limit>`
2. Initialize batch state:
   - `detail_batch_driver.py init <task_dir>`
3. Get next item:
   - `detail_batch_driver.py next <task_dir>`
4. Open the returned item URL with the browser tool.
5. Snapshot the page and save it to `detail-N.txt`.
6. Process it:
   - `browser_detail_processor.py <task_dir> <detail-N.txt> <detail_url> <source_item_link>`
7. Mark success:
   - `detail_batch_driver.py done <task_dir>`
8. On failure:
   - save screenshot / note if available
   - `detail_batch_driver.py fail <task_dir> <reason>`
9. Repeat until `done=true`.

## Outputs
- `detail_queue.json`
- `detail_batch_state.json`
- `detail_failures.json`
- `detail_results.jsonl`

## Why this matters
This turns detail extraction from one-off manual enrichment into a repeatable queue-driven workflow.
