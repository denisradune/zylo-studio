#!/usr/bin/env bash
# One-time (or fresh-container) setup: toolkit, Python env, voice model, Remotion.
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)

TOOLKIT=${TOOLKIT_DIR:-$ROOT/../digitalsamba/claude-code-video-toolkit}
if [ ! -d "$TOOLKIT/.git" ]; then
  mkdir -p "$(dirname "$TOOLKIT")"
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/digitalsamba/claude-code-video-toolkit "$TOOLKIT"
fi

[ -x .venv/bin/python ] || uv venv -q .venv
uv pip install -q --python .venv/bin/python -r requirements.txt

mkdir -p .models
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s ".models/$f" ] || curl -sSL -o ".models/$f" "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done

(cd templates && [ -d node_modules ] || npm install --no-audit --no-fund)
echo "zylo studio ready"
