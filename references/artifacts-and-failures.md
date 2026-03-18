# Artifacts and Failures

Use artifacts to make runs inspectable and resumable.

## Artifact classes
- snapshot text files
- screenshots
- browser plans
- runtime state files
- results.jsonl / detail_results.jsonl
- reports

## Files
- `artifacts_manifest.json`
- `failure_artifacts.json`

## Recommended behavior
- record every important snapshot file
- record screenshots on failure
- record the failing URL and a human-readable reason
- keep artifacts inside the task dir so the entire run is portable

## Scripts
- `artifact_recorder.py artifact <task_dir> <kind> <path> [url] [note]`
- `artifact_recorder.py failure <task_dir> <url> <reason> [snapshot_path] [screenshot_path]`
