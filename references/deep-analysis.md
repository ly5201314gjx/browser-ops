# Deep Analysis（深层次解析）

## 作用

Deep Analysis 用于在普通页面侦察之上，进一步对网站进行结构化深挖。  
它不是简单的“多看几眼页面”，而是输出可用于：

- route judgement
- action policy tuning
- handoff explanation
- recovery decisions
- profile generation
- long-term site strategy

的深层站点情报。

当前会产出：
- `deep_analysis.json`
- `deep_report.md`

---

## 8 个维度

### 1. 页面结构（Page Structure）
识别：
- heading / link / input / button 密度
- iframe / modal / dialog 信号
- 交互区域分布

### 2. 数据流（Data Flow）
识别：
- search flow
- pagination flow
- client storage
- runtime state keys

### 3. 网络依赖（Network Dependencies）
识别：
- first-party APIs
- third-party APIs
- API-like paths
- 依赖链数量

### 4. 状态机（State Machine）
识别：
- empty / loading / error / success / login 等状态
- blocking states
- route implications

### 5. 交互复杂度（Interaction Complexity）
用于估计：
- automation difficulty
- recommended mode
- 是否需要更保守策略

### 6. 安全与拦截（Security Barriers）
识别：
- login wall
- captcha
- MFA
- approval gate
- anti-automation / cross-origin friction

### 7. 可提取性（Extractability）
判断：
- 结构稳定度
- 是否存在重复项
- 是否值得生成 profile
- 推荐字段与建议路线

### 8. 产品意图（Product Intent）
推断：
- core CTA
- product guess
- 站点的真实用途

---

## 使用时机

在这些场景优先跑 Deep Analysis：

- 用户明确说“深挖 / 深层解析 / 深度研究这个网站”
- 网站结构复杂，需要先理解再自动化
- 需要判断到底该走 HTTP、Browser、Hybrid 还是 Human
- 想决定一个站值不值得做 reusable profile
- 想让 recovery / handoff / policy 更聪明

---

## 当前接入点

Deep Analysis 结果目前已经进入：

- intelligence bootstrap
- report builder
- runbook builder
- handoff packet
- failure recovery engine
- recovery runbook builder
- autopilot tick
- browser next step
- action policy engine

这意味着它已经不是孤立报告，而是正式的决策输入。

---

## Phase 1 限制

当前是可用版，不是最终完整版：

- 8 维逻辑目前主要集中在 `deep_analysis_engine.py`
- 还没有拆成每维一个独立模块
- 网络链和浏览器 runtime 结合仍可继续增强
- 评分体系还可以继续细化

所以使用定位是：

> **能用、能产物、能进入决策链，但后续还可以继续做成完整引擎。**
