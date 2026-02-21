#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "[$(date -u +'%Y-%m-%d %H:%M:%S') UTC] Starting local sync..."

# 1) Pull fresh Telegram topic data
rye run python export_topic.py

# 2) Enrich YouTube metadata
rye run python enrich_youtube.py

# 3) Commit + push only if tracked output files changed
git add data.json data_enriched.json
if git diff --staged --quiet; then
  echo "[$(date -u +'%Y-%m-%d %H:%M:%S') UTC] No changes to commit."
  exit 0
fi

git commit -m "Local auto-update at $(date -u +'%Y-%m-%d %H:%M:%S') UTC"
git push

echo "[$(date -u +'%Y-%m-%d %H:%M:%S') UTC] Sync completed and pushed."
