#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$PROJECT_DIR/run_local_sync.sh"
LOG_FILE="$PROJECT_DIR/local_update.log"
LOCK_FILE="/tmp/cook-local-sync.lock"
CRON_LINE="*/2 * * * * cd $PROJECT_DIR && /usr/bin/flock -n $LOCK_FILE $RUNNER >> $LOG_FILE 2>&1"

if [[ ! -x "$RUNNER" ]]; then
  chmod +x "$RUNNER"
fi

TMP_CRON="$(mktemp)"
crontab -l 2>/dev/null | grep -v "cook-local-sync.lock" > "$TMP_CRON" || true
echo "$CRON_LINE" >> "$TMP_CRON"
crontab "$TMP_CRON"
rm -f "$TMP_CRON"

echo "Installed local cron job:"
echo "$CRON_LINE"
echo ""
echo "Verify with: crontab -l"
echo "Logs at: $LOG_FILE"
