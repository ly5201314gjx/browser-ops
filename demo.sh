#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TASK_DIR="/tmp/browser_ops_demo_release"
PROFILE="$ROOT/assets/example_profiles/hackernews-browser.json"

echo "[1/6] Cleaning demo dir..."
rm -rf "$TASK_DIR"
mkdir -p "$TASK_DIR"

echo "[2/6] Applying device profile..."
python3 "$ROOT/scripts/device_profile_manager.py" "$TASK_DIR" mobile-default >/dev/null

echo "[3/6] Enabling human mode..."
python3 "$ROOT/scripts/browser_human_mode.py" enable "$TASK_DIR" human-assisted balanced >/dev/null

echo "[4/6] Building action policy..."
python3 "$ROOT/scripts/action_policy_engine.py" "$TASK_DIR" "$PROFILE" >/dev/null

echo "[5/6] Init orchestrator..."
python3 "$ROOT/scripts/browser_ops_orchestrator.py" init "$PROFILE" "$TASK_DIR" 3 2 false >/dev/null

echo "[6/6] Build plan / runbook / handoff payload..."
python3 "$ROOT/scripts/browser_plan_builder.py" "$PROFILE" "$TASK_DIR" >/dev/null
python3 "$ROOT/scripts/browser_runbook_builder.py" "$TASK_DIR" >/dev/null
python3 "$ROOT/scripts/browser_handoff_payload.py" "$TASK_DIR" >/dev/null

echo
echo "✅ Demo prepared successfully."
echo "Task dir: $TASK_DIR"
echo "Artifacts:"
echo "  - $TASK_DIR/action_policy.json"
echo "  - $TASK_DIR/browser_plan.json"
echo "  - $TASK_DIR/runbook.json"
echo "  - $TASK_DIR/browser_handoff_payload.json"
echo
echo "如果你想把它交给自己的 OpenClaw 使用："
echo "1) 保持仓库目录结构完整（SKILL.md / assets / references / scripts）"
echo "2) 让 OpenClaw 能读到这个项目目录"
echo "3) 以 browser-ops skill 方式调用对应脚本或参考 SKILL.md"
