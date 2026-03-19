# Demo Showcase

## 一眼看懂 Browser Ops 的运行方式

### 正常路径
1. intelligence 看懂页面
2. orchestrator 选择 route
3. action policy 注入计划与 runbook
4. autopilot 推进非-browser部分
5. browser handoff payload 接住 browser slice
6. report 收尾

### 异常路径
1. 失败登记成 incident
2. recovery system 分类问题
3. retry budget / cooldown 生效
4. recovery plan 生成
5. recovery runbook 引导恢复
6. 条件满足时 auto-resolve
