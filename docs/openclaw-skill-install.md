# 如何把 Browser Ops 交给你自己的 OpenClaw（龙虾）

## 目标
让 OpenClaw 能把这个项目识别成一个技能，并按 `SKILL.md` 的结构来使用它。

## 最简单的方法
1. 克隆仓库
2. 运行：`bash install.sh`
3. 确认：`browser-ops doctor`
4. 保持项目目录结构完整：
   - `SKILL.md`
   - `assets/`
   - `references/`
   - `scripts/`
5. 让 OpenClaw 能读取到该目录

## 为什么它能被识别成技能？
因为它已经具备 OpenClaw 友好的技能布局：
- 顶层 `SKILL.md`
- 资源分层清晰
- 参考文档与脚本可直接寻址
- 项目结构稳定，适合被技能系统读取

## 建议
- 不要随意打乱目录结构
- 不要删除 `SKILL.md`
- 优先通过 `browser-ops doctor` 检查交付包完整性
