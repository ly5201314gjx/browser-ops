# Site Connectivity Adapter

Site Connectivity Adapter 是 Browser Ops 的站点连通性适配层。

## 它解决什么问题？
- 某些站点直连超时
- 某些环境需要走用户自有代理
- 某些站点需要备用入口或镜像地址
- 需要在 browser workflow 之前先做连通性探测

## 它不做什么？
- 不绕过访问控制
- 不绕过平台安全机制
- 不承诺“万能打开所有网站”
- 不提供对抗风控能力

## 机制
1. direct 直连尝试
2. mirror/fallback base URL 尝试
3. 用户自有代理（通过环境变量）尝试
4. retries + backoff
5. 输出 `connectivity_report.json`
6. 可接入 orchestrator / runbook，作为正式前置检查步骤
7. connectivity failure 可进入 recovery system 分类与恢复规划

## 配置
在 profile 中可设置：
- `connectivity.timeoutSeconds`
- `connectivity.retries`
- `connectivity.backoffMs`
- `connectivity.proxyEnv`
- `connectivity.fallbackBaseUrls`
