# Workflow Recipes

## Recipe 1: List crawl
1. Open list page
2. Extract item cards
3. Normalize titles/links
4. Paginate until maxPages or no next page
5. Save results.jsonl and failed_urls.json

## Recipe 2: List + detail enrichment
1. Run list crawl
2. Deduplicate links
3. Visit each detail page
4. Extract detail fields
5. Merge into structured output

## Recipe 3: Human-assisted login then continue
1. Open login page
2. Fill what is safe and deterministic
3. Stop before captcha/MFA/approval wall
4. Ask the human to complete the checkpoint
5. Resume automation after the checkpoint

## Recipe 4: Hybrid API discovery
1. Open target page in browser
2. Observe inline data and network patterns
3. Identify stable JSON/API payloads
4. Switch repeated extraction to HTTP route
5. Keep browser only for session bootstrap if needed
