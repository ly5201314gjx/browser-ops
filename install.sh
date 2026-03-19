#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "[1/7] Checking Python..."
command -v "$PYTHON_BIN" >/dev/null 2>&1 || { echo "Python not found: $PYTHON_BIN"; exit 1; }
"$PYTHON_BIN" --version

echo "[2/7] Creating virtualenv..."
"$PYTHON_BIN" -m venv "$VENV"

# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "[3/7] Upgrading pip / build tools..."
pip install --upgrade pip setuptools wheel >/dev/null

echo "[4/7] Installing requirements..."
pip install -r "$ROOT/requirements.txt" >/dev/null

echo "[5/7] Installing Browser Ops CLI..."
pip install -e "$ROOT" >/dev/null

echo "[6/7] Running doctor..."
python "$ROOT/scripts/doctor.py"

echo "[7/7] Running smoke test..."
python "$ROOT/scripts/smoke_test.py"

echo
echo "✅ Browser Ops install finished."
echo "Activate with: source $VENV/bin/activate"
echo "Try CLI with: browser-ops doctor"
echo "Run demo with: browser-ops demo"
