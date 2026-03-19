# Browser Ops 工作流图（文字版）

```text
intelligence
   ↓
list
   ↓
detail-queue
   ↓
detail
   ↓
report
```

## 关键旁路
- intelligence 可改写 effectiveRoute
- autopilot 负责非-browser推进
- browser boundary 触发 handoff payload
- failure recovery system 负责异常路径恢复
