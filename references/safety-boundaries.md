# Safety Boundaries

## Allowed
- Browser automation on sites the user is authorized to use
- Public-page crawling within reasonable rate limits
- Human-assisted workflows for login, MFA, approval, or consent checkpoints
- Discovering site APIs by observing normal page behavior

## Not allowed
- Building captcha bypass tooling
- Circumventing MFA or access control
- Evading platform security protections
- Running abusive, high-rate scraping without bounds
- Pretending to be a human to defeat protections

## Default behavior when protected checkpoints appear
1. stop automated progression
2. capture state and screenshot
3. report exactly what needs human action
4. resume only after human confirmation/action
