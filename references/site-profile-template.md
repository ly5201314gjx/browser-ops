# Site Profile Template

Use one profile per recurring site/task.

```json
{
  "name": "example-site",
  "route": "browser",
  "startUrls": ["https://example.com/list"],
  "allowedDomains": ["example.com"],
  "requiresLogin": false,
  "humanCheckpoints": {
    "captcha": true,
    "mfa": true,
    "approval": true
  },
  "rateLimitMs": 1200,
  "maxPages": 20,
  "list": {
    "itemSelector": "article.card",
    "fallbackItemSelectors": [".card", "li.result"],
    "titleSelector": "h2 a",
    "linkSelector": "h2 a",
    "summarySelector": ".summary",
    "nextPageSelector": "a.next"
  },
  "detail": {
    "titleSelector": "h1",
    "contentSelector": "article",
    "timeSelector": "time",
    "authorSelector": ".author",
    "tagSelector": ".tags a"
  },
  "extraction": {
    "preferEmbeddedJson": true,
    "preferNetworkDiscovery": true,
    "captureScreenshotsOnFailure": true,
    "outputFormat": "jsonl"
  }
}
```

## Notes

- `route`: one of `http`, `browser`, `hybrid`, `human`.
- `humanCheckpoints`: if true, stop and request human action instead of trying to bypass.
- `fallbackItemSelectors`: use when the primary selector breaks.
- `preferEmbeddedJson`: inspect inline JSON/script data before expensive DOM traversal.
- `preferNetworkDiscovery`: if browser reveals a stable API, migrate repeated bulk pulls away from DOM scraping.
