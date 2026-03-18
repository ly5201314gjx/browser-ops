# Browser Ops 🚀🌐

> 一个把 **浏览器自动化、结构化采集、人机协同、动作策略、失败恢复** 真正揉成“平台内核”的 OpenClaw Browser Operations Platform。

如果你想做的不只是“写几个 Playwright 脚本”，而是想要一个：

- 能看懂页面 🧠
- 能决定路线 🧭
- 能产出 runbook 📋
- 能半自动推进 ⚙️
- 能做人机协同 🤝
- 能在失败后体面恢复 ♻️

那这个项目就是冲着这个目标狠狠干出来的。

---

## ✨ 这玩意到底是什么？

`browser-ops` 不是单点爬虫，不是一次性脚本，也不是“点点点自动化小玩具”。

它的定位是：

### **OpenClaw Browser Operations Platform**

一个围绕浏览器工作流的**平台级技能 / 内核层系统**，核心目标是把复杂浏览器任务拆成：

1. **页面侦察（intelligence）**
2. **路线决策（route selection）**
3. **动作策略（action policy）**
4. **执行与交接（runbook / handoff）**
5. **自动推进（autopilot）**
6. **失败恢复（recovery system）**

最后形成一个可恢复、可观察、可扩展、可展示、可复用的浏览器工作流平台。🔥

---

## 💥 项目亮点

### 1. Site Intelligence：先看懂页面，再决定怎么干
- 判断页面更像 list / detail / login / search / dashboard
- 检测 login / MFA / captcha / approval checkpoints
- 给出 `recommendedRoute`
- 产出 profile draft

### 2. Intelligence-Aware Orchestrator：分析结果直接影响执行路径
- intelligence-first 初始化
- `effectiveRoute` 驱动 browser / http / human
- phase 化推进：`intelligence → list → detail-queue → detail → report`

### 3. Action Policy Layer：不是只会做，还知道怎么更稳地做
- device profiles（desktop / mobile / tablet）
- interaction timing / touch rhythm / motion / bounded randomization
- profile strategy fields：
  - `preferredDevice`
  - `navigationStyle`
  - `riskTolerance`
  - `checkpointPolicy`
  - `interactionPolicy`

### 4. Human-Collab Real-Device Mode：人机协同不是口头说说
- `handoff_packet.json`
- `browser_handoff_payload.json`
- device-aware interaction plan
- protected checkpoint 停靠与 resume

### 5. Autopilot Mode：自动推进非浏览器胶水工作
- 自动 rebuild runbook
- 自动执行非-browser步骤
- 遇 browser boundary 优雅停下
- 保留 blockedAfterBrowser 语义

### 6. Failure Recovery System：失败不是结束，而是另一条工作流
- incident registry
- recovery state / plan / runbook
- failure classification
- retry budgets / cooldown
- auto-resolve hooks

---

# 🧠 真实算法机制介绍

## 一、路由决策内核（Routing Kernel）

`browser-ops` 会先通过 `site_intelligence.py` 分析页面，再让 orchestrator 用 `effectiveRoute` 驱动后续行为。

### 路由类型
- `http`
- `browser`
- `hybrid`
- `human`

### 决策原则
- 能 HTTP 就别硬上 browser
- 能 browser 就别做脏绕过
- 碰到 login / MFA / captcha / approval，就切 human-in-the-loop
- intelligence 不是旁路报告，而是直接影响 runbook / route / phase

---

## 二、动作策略内核（Action Policy Kernel）

这部分不是“绕风控”，而是**合规的动作参数真实化与一致化**。

### 输入层
- device profile
- site profile strategy fields
- human mode policy
- interaction policy defaults / overrides

### 输出层
统一生成 `action_policy.json`，内容包括：
- `device`
- `navigationStyle`
- `riskTolerance`
- `checkpointPolicy`
- `interactionPolicy`

### 作用
再把这些参数注入：
- `browser_plan.json`
- `runbook.json`
- `handoff_packet.json`
- `browser_handoff_payload.json`

### 典型参数
- `pageSettleMs`
- `elementConfirmPauseMs`
- `betweenActionsMs`
- `downDelayMs`
- `multiTouchGapMs`
- `swipeDurationMs`
- `inertia`
- `timeJitterPct`

---

## 三、自动推进内核（Autopilot Kernel）

Autopilot 不假装“全自动浏览器”，而是做更聪明的事：

### 它会自动做
- rebuild runbook
- 执行所有非-browser步骤
- 生成 browser handoff payload
- 停在 browser boundary

### 它不会乱做
- 不伪造浏览器动作已经完成
- 不在 browser step 未完成时继续执行依赖步骤

这意味着系统能清楚区分：
- **可自动推进部分**
- **必须交接的人/浏览器切片**

---

## 四、失败恢复内核（Recovery Kernel）

这是整个项目最有“平台感”的部分之一。💣

### 不是简单记日志，而是：
1. 把失败登记成 incident
2. 自动分类 failure category
3. 为不同类型分配 retry budget / cooldown
4. 根据当前 workflow state 构建 recovery plan
5. 产出 recovery runbook
6. 条件满足时触发 auto-resolve hook

### 当前支持的失败分类
- `browser-boundary-interruption`
- `missing-artifact`
- `parser-failure`
- `route-mismatch`
- `detail-batch-failure`
- `report-generation-failure`
- `unknown-failure`

### 当前支持的恢复动作
- `resume-browser-slice`
- `retry-last-failed-slice`
- `human-review`
- `resume-detail-index`
- `resume-list-phase`
- `rebuild-report`
- `auto-resolve-incident`

这让 browser-ops 不只是“能跑”，而是**炸了以后还知道怎么优雅恢复**。♻️

---

# 🧱 真实内核分层

## Layer 1 — Intelligence
- 页面识别
- route recommendation
- profile bootstrapping

## Layer 2 — Orchestration
- phase state machine
- effectiveRoute
- next-action generation

## Layer 3 — Action Policy
- device posture
- navigation style
- interaction timing / motion
- checkpoint policy

## Layer 4 — Execution
- list processing
- detail enrichment
- pagination loop
- batch detail queue

## Layer 5 — Handoff
- human handoff packet
- browser handoff payload
- browser boundary semantics

## Layer 6 — Recovery
- incident registry
- retry budgets
- cooldown windows
- recovery runbooks
- auto-resume hooks

---

# 🛡️ 安全边界

这个项目**明确不做**：
- captcha bypass
- MFA/access-control bypass
- evading platform security protections
- pretending to be a human to defeat protections

遇到这些情况，正确路线永远是：
- 停下
- 存档
- handoff
- resume

这不是怂，这是平台级系统该有的边界感。✅

---

# 📦 目录结构

```text
browser-ops/
├── SKILL.md
├── assets/
├── references/
└── scripts/
```

你会看到几类关键文件：

### 核心脚本
- `site_intelligence.py`
- `browser_ops_orchestrator.py`
- `browser_runbook_builder.py`
- `autopilot_tick.py`
- `action_policy_engine.py`
- `browser_handoff_payload.py`
- `failure_recovery_engine.py`
- `recovery_runbook_builder.py`

### 关键文档
- `references/intelligence-first-flow.md`
- `references/action-policy-layer.md`
- `references/browser-handoff-payload.md`
- `references/failure-recovery-system.md`

---

# 🚀 为什么这个项目可能让人想点 Star？

因为它想解决的不是“浏览器自动化能不能点按钮”，而是：

> **怎么把浏览器任务做成真正可运营、可恢复、可交接、可观察的平台系统。**

很多项目停在“脚本能跑”。

这个项目往前多走了几步：
- 让 intelligence 进入决策层
- 让 action policy 进入 plan / runbook / handoff
- 让 autopilot 知道 browser boundary
- 让 failure recovery 成为正式内核

这几步一叠起来，味道就不一样了。✨

---

# ⚡ 快速开始

> 这是 OpenClaw skill 形态项目，最适合在 OpenClaw 环境中使用。

## 基本流程
1. 准备站点 profile
2. 初始化 task dir
3. 跑 orchestrator / runbook
4. 用 browser tool 完成 browser slice
5. 用 autopilot 推进非-browser slice
6. 出问题就走 recovery plan / recovery runbook

---

# 📣 最后

如果你也烦透了那些：
- 只能 demo 一次的脚本
- 没状态、没恢复、没交接的浏览器自动化
- 一炸就得人脑从头排查的工作流

那 `browser-ops` 这条路线，可能会让你眼前一亮。👀

欢迎 star / fork / issue / 一起把这玩意继续狠狠干大。🔥🔥🔥
