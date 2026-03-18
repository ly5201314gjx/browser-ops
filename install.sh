#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV="$ROOT/.venv"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "[1/5] Checking Python..."
command -v "$PYTHON_BIN" >/dev/null 2>&1 || { echo "Python not found: $PYTHON_BIN"; exit 1; }
"$PYTHON_BIN" --version

echo "[2/5] Creating virtualenv..."
"$PYTHON_BIN" -m venv "$VENV"

# shellcheck disable=SC1091
source "$VENV/bin/activate"

echo "[3/5] Upgrading pip..."
pip install --upgrade pip >/dev/null

echo "[4/5] Installing requirements..."
pip install -r "$ROOT/requirements.txt" >/dev/null

echo "[5/5] Running doctor..."
python "$ROOT/scripts/doctor.py"

echo
echo "✅ Browser Ops install finished."
echo "Activate with: source $VENV/bin/activate"
echo "Run demo with: bash $ROOT/demo.sh"
