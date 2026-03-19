# Browser Ops 架构图（文字版）

```text
User / Agent
   │
   ▼
Site Intelligence
(页面类型 / 检查点 / 路线判断)
   │
   ▼
Deep Analysis (8 dimensions)
(页面结构 / 数据流 / 网络依赖 / 状态机 /
 交互复杂度 / 安全与拦截 / 可提取性 / 产品意图)
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
(device + strategy + checkpoint + timing + motion + deep-analysis posture)
            │
            ▼
Workflow Layer
(plan + runbook + handoff payload + recovery runbook)
            │
            ├── Execution Layer
            │     ├── list/detail processors
            │     ├── queue / batch drivers
            │     └── crawlers
            │
            ├── Control Layer
            │     ├── next step
            │     ├── state driver
            │     ├── autopilot
            │     ├── human mode
            │     └── handoff packet
            │
            └── Browser Slice / Human Slice
                  (browser tool / agent / human-in-the-loop)
                        │
                        ▼
Failure Recovery System
(incident registry + recovery plan + recovery runbook + retry budget + auto-resume hooks)
                        │
                        ▼
Reporting Layer
(report.md + deep_report.md + artifacts + state)
```

## 分层说明

### 1. Intelligence Layer
负责识别页面类型、拦截点、分页信号、嵌入数据和推荐路线。

### 2. Deep Analysis Layer
负责做 8 维深层次解析，并输出：
- `deep_analysis.json`
- `deep_report.md`

这一层已经接入：
- intelligence bootstrap
- report builder
- runbook
- handoff
- recovery
- autopilot
- next-step
- action policy

### 3. Policy Layer
根据：
- profile
- device profile
- human mode
- deep analysis difficulty

生成更保守或更激进的动作策略。

### 4. Workflow Layer
把任务转成：
- browser plan
- runbook
- handoff payload
- recovery runbook

让任务从“一次性脚本”变成“可恢复、可交接、可继续推进的工作流”。

### 5. Execution Layer
负责实际的数据抽取和页面处理：
- list pages
- detail pages
- queue/batch
- http route
- crawl orchestration

### 6. Control Layer
负责控制推进逻辑：
- next-step 建议
- browser runtime state
- autopilot
- human-mode
- handoff packet

### 7. Recovery Layer
负责失败分类、重试预算、恢复计划、人工 review 触发与恢复 runbook。

### 8. Reporting Layer
负责统一沉淀：
- `report.md`
- `deep_report.md`
- artifacts
- runtime state
- failure evidence

## 当前核心链路

Browser Ops 当前主链路已经是：

```text
Site Intelligence
  -> Deep Analysis
  -> Action Policy
  -> Runbook / Handoff / Recovery
  -> Autopilot / Next Step
  -> Reporting
```

这意味着 Browser Ops 已经不是普通的浏览器自动化脚本集合，而是一个：

> **情报驱动、策略可调、可恢复、可交接、可深挖的网站操作平台。**
