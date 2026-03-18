# Browser Ops for OpenClaw 🚀

<p align="center">
  <img src="docs/hero-banner.svg" alt="Browser Ops Hero Banner" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/ly5201314gjx/browser-ops/stargazers"><img src="https://img.shields.io/github/stars/ly5201314gjx/browser-ops?style=for-the-badge" /></a>
  <a href="https://github.com/ly5201314gjx/browser-ops/releases"><img src="https://img.shields.io/github/v/release/ly5201314gjx/browser-ops?style=for-the-badge" /></a>
  <a href="https://github.com/ly5201314gjx/browser-ops/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ly5201314gjx/browser-ops?style=for-the-badge" /></a>
  <img src="https://img.shields.io/badge/OpenClaw-Native-7C3AED?style=for-the-badge" />
  <img src="https://img.shields.io/badge/HITL-First%20Class-F59E0B?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Recovery-Incident%20Aware-22C55E?style=for-the-badge" />
</p>

<p align="center">
  <b>不是浏览器脚本集合，不是一次性自动化玩具，不是炸了就重跑的 Demo 仓库。</b><br/>
  <b>这是一个专门为 OpenClaw 打造的 Browser Workflow Kernel。🔥</b><br/>
  <b>能理解页面、选择路线、携带策略、优雅交接、自动推进、失败恢复。</b>
</p>

---

## 这到底是什么？🧠

`Browser Ops for OpenClaw` 是一个围绕浏览器任务构建的**平台级工作流内核**。  
它不是一次性脚本，不是只会点按钮的自动化玩具，也不是“写完就忘”的临时爬虫集合。

它真正要解决的问题是：

> **怎么把浏览器任务，做成一个可观察、可恢复、可交接、可持续进化的系统。**

很多项目只能做到：
- 打开页面
- 点几个按钮
- 抓一点数据
- 一出错就手工排查 😵

而 Browser Ops 想做的是更高一个层级的事情：
- 先看懂页面，再决定路线 🧭
- 让不同站点走不同策略，而不是一把梭 ⚙️
- 遇到浏览器边界时优雅停下，而不是乱撞 ✋
- 能把任务交给人、交给代理、再继续推进 🤝
- 失败后不是“重来一遍”，而是有恢复计划、有重试预算、有恢复剧本 ♻️

这就是它的核心价值。

---

## 为什么它很不一样？💥

因为它不是把“浏览器自动化”当成几个脚本文件，  
而是把它当成一个**真正的系统问题**来做。

### 普通浏览器项目通常只关心：
- 能不能打开网页
- 能不能点击
- 能不能抓到内容

### Browser Ops 关心的是：
- 页面现在到底是什么类型？
- 该走 HTTP、Browser、Hybrid 还是 Human Route？
- 当前动作节奏、设备姿态、交互参数应该是什么？
- 哪些步骤可以自动推进？哪些必须停在 browser boundary？
- 如果失败了，怎么恢复最合理？
- 如果需要人接手，怎么把上下文和策略完整交过去？

这就让它从“能跑的脚本”，升级成了：

> **专门为 OpenClaw 服务的浏览器工作流平台。** 🚀

---

## 它能干什么？✨

### 1）页面侦察（Site Intelligence）
系统会先分析页面，再判断它更像：
- 列表页
- 详情页
- 登录页
- 搜索页
- 需要人工介入的检查点

这样做的好处是：
**不是一上来就瞎执行，而是先看懂再动手。**

---

### 2）路线决策（Route Selection）
根据页面状态和任务需求，系统会决定走哪条路线：
- `HTTP`：能直接拿数据，就别浪费浏览器资源
- `Browser`：必须渲染、点击、滚动、交互时再上
- `Hybrid`：先用浏览器侦察，再切回 HTTP 做高效采集
- `Human`：碰到登录、MFA、验证码、审批墙时，老老实实停下

这意味着：
**它不是死脑筋自动化，而是会选路。** 🧭

---

### 3）动作策略层（Action Policy Layer）
这部分非常关键。  
它会把：
- 设备类型（桌面 / 手机 / 平板）📱💻
- 页面操作节奏
- 点击/滑动/停顿参数
- 检查点策略
- 风险容忍度

统一揉成一个 `action_policy.json`。

然后再把这套策略注入到：
- 浏览器执行计划
- runbook
- handoff payload
- 恢复流程

也就是说，系统不只是知道“下一步做什么”，
还知道：

> **应该用什么姿态、什么节奏、什么边界来做。**

这就是专业性。

---

### 4）人机协同（Human-in-the-Loop）🤝
真正复杂的浏览器任务，永远不可能 100% 靠硬跑解决。

所以 Browser Ops 把“人机协同”做成了一等公民：
- `handoff_packet.json`
- `browser_handoff_payload.json`
- browser boundary 语义
- resume 流程

小白也能理解成一句话：

> **该自动的时候自动，该停的时候停，该交给人时就交得清清楚楚。**

不会出现那种“系统卡住了但你根本不知道该接什么”的傻情况。

---

### 5）自动推进（Autopilot）⚙️
Autopilot 不是假装“全自动浏览器”，而是做更聪明的事：

- 自动重建 runbook
- 自动推进非浏览器部分
- 遇到浏览器边界立即停下
- 把后续依赖步骤标记为 blocked

这让整个系统非常清楚地知道：
- 哪部分能自己推进
- 哪部分必须靠浏览器动作完成
- 哪部分完成后才能继续

这不是偷懒，反而是更专业的工作流设计。

---

### 6）失败恢复系统（Failure Recovery System）♻️
这是整个项目最狠的一块之一。

很多项目失败之后，所谓“恢复”其实就是：
- 报个错
- 打个日志
- 人自己看着办

Browser Ops 不是这样。

它会把失败当成正式事件处理：
- 注册 incident
- 分类 failure category
- 分配 retry budget
- 增加 cooldown window
- 生成 recovery plan
- 产出 recovery runbook
- 条件满足时自动触发 auto-resolve hook

说白了就是：

> **失败不是终点，而是另一条有组织的工作流。**

这就是平台级系统该有的味道。🔥

---

## 真实算法介绍（简洁版）⚙️

### 1. 路由内核（Route Kernel）
先分析页面，再生成 `recommendedRoute`，决定走：
- HTTP
- Browser
- Hybrid
- Human

### 2. 动作策略内核（Action Policy Kernel）
把设备画像、站点策略、人机协同策略、交互默认参数合并成统一策略层，输出到计划、runbook 和 handoff payload 中。

### 3. 浏览器边界模型（Browser Boundary Model）
一旦进入 browser-controlled slice：
- autopilot 停止
- 保留 `pendingBrowserSteps`
- 标记 `blockedAfterBrowser`
- 生成 handoff payload

### 4. 恢复内核（Recovery Kernel）
故障出现后，系统会：
- 记录 incident
- 自动分类
- 应用重试预算和冷却窗口
- 构建 recovery plan
- 生成 recovery runbook
- 满足条件时自动恢复或自动关单

这四个内核加起来，才构成 Browser Ops 的真实机制。🧠

---

## 一眼看懂它为什么猛 ⚡

因为它不是只解决“浏览器能不能自动化”，而是在解决更本质的事：

- **任务开始前**：先理解页面，不盲点 🧠
- **任务推进时**：按 route 和 action policy 执行，不乱跑 ⚙️
- **任务交接时**：有 handoff payload，不掉上下文 📦
- **任务失败后**：有 incident / recovery / retry budget，不靠运气 ♻️

一句话：

> **Browser Ops for OpenClaw = 浏览器任务的工作流内核，而不是几个自动化脚本。**

---

## Demo 展示 👀

- [Demo Showcase](docs/demo-showcase.md)

---

## 架构与工作流图 🗺️

- [架构图（SVG）](docs/architecture.svg)
- [工作流图（SVG）](docs/workflow.svg)
- [架构说明](docs/architecture.md)
- [工作流说明](docs/workflow.md)

---

## 快速开始 ⚡

> 这个项目是为 **OpenClaw** 专门打造的，最适合在 OpenClaw 环境中使用。

### 初始化任务目录
```bash
python3 scripts/browser_ops_orchestrator.py init assets/example_profiles/hackernews-browser.json /tmp/browser_ops_demo 3 2 true
```

### 生成 runbook
```bash
python3 scripts/browser_runbook_builder.py /tmp/browser_ops_demo
```

### 自动推进非浏览器部分
```bash
python3 scripts/autopilot_tick.py /tmp/browser_ops_demo
```

### 浏览器切片交接
```bash
python3 scripts/browser_handoff_payload.py /tmp/browser_ops_demo
```

### 失败恢复
```bash
python3 scripts/failure_recovery_engine.py plan /tmp/browser_ops_demo
python3 scripts/recovery_runbook_builder.py /tmp/browser_ops_demo
```

---

## 为什么它是 OpenClaw 专用项目？🌊

因为它从一开始就不是为了做“通用脚本大杂烩”。

它是围绕 OpenClaw 的这些能力设计出来的：
- skill 体系
- browser tool
- runbook 模型
- session workflow
- human-in-the-loop 协同
- 状态文件 + 恢复链路

所以这不是“把浏览器自动化塞进 OpenClaw”。

而是：

> **为 OpenClaw 原生长出来的一套 Browser Operations 内核。**

这点非常重要，也正是这个仓库最值钱的地方之一。✨

---

## 安全边界 🛡️

这个项目明确不做：
- captcha bypass
- MFA / access-control bypass
- 绕平台安全机制
- 伪装真人去对抗检测

遇到这些情况，正确做法永远是：
- 停下
- 留痕
- handoff
- resume

边界清楚，系统才可信。✅

---

## Roadmap 🛣️

### v0.1.0
- intelligence-aware orchestrator
- action policy layer
- human-collab handoff
- browser boundary model
- failure recovery system

### v0.2.0
- site-specific recovery heuristics
- browser slice resume hooks
- stronger parser/profile overrides
- richer recovery lineage

### v0.3.0
- visual dashboards
- stronger hybrid route adapters
- more showcase profiles
- policy-aware browser execution adapters

---

## 最后说一句 🔥

如果你想找的只是一个“会点网页的脚本项目”，那 GitHub 上这种仓库太多了。

但如果你要的是：
- 更像系统内核
- 更像工作流平台
- 更像真正能跑、能停、能交接、能恢复的浏览器能力层

那 Browser Ops for OpenClaw 走的，就是这条路。  
而且这条路，不是随便写写，是狠狠干出来的。⚡

如果你也认这条路线，欢迎 ⭐ Star / Fork / Issue / Discussion。  
一起把它继续干大。🚀
