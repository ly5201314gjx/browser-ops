# Browser Ops 架构图（文字版）

```text
User / Agent
   │
   ▼
Site Intelligence
   │
   ▼
Orchestrator / effectiveRoute
   ├── HTTP Route
   ├── Browser Route
   ├── Hybrid Route
   └── Human Route
            │
            ▼
Action Policy Layer
(device + strategy + checkpoint + timing + motion)
            │
            ▼
Runbook / Browser Handoff Payload / Handoff Packet
            │
            ├── Autopilot (non-browser)
            └── Browser Slice (human/agent/browser tool)
                        │
                        ▼
Failure Recovery System
(incident registry + recovery plan + recovery runbook + retry budget + auto-resume hooks)
```
