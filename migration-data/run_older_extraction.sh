#!/bin/bash
# Overnight runner for extract_erlang_factory.py --all.
# The extractor is idempotent/resumable (existing assets skipped), so on any
# failure (wifi drop, Wayback hiccup) we just re-invoke it, up to MAX tries.
# Log: migration-data/older-extract.log
set -u
cd "$(dirname "$0")/.."
LOG=migration-data/older-extract.log
MAX=8
for attempt in $(seq 1 $MAX); do
  echo "=== attempt $attempt/$MAX  $(date '+%F %T') ===" | tee -a "$LOG"
  if python3 migration-data/extract_erlang_factory.py --all >>"$LOG" 2>&1; then
    echo "=== SUCCESS $(date '+%F %T') ===" | tee -a "$LOG"
    exit 0
  fi
  echo "=== attempt $attempt failed, sleeping 120s ===" | tee -a "$LOG"
  sleep 120
done
echo "=== GAVE UP after $MAX attempts $(date '+%F %T') ===" | tee -a "$LOG"
exit 1
