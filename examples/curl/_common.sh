# Shared by the curl examples. Test mode only.
set -euo pipefail
: "${AGILIS_API_KEY:?Set AGILIS_API_KEY to your Test API key (pk_test_...).}"
case "$AGILIS_API_KEY" in
  pk_test_*) ;;
  *) echo "These examples run in Test mode only: use a key that starts with pk_test_." >&2; exit 1 ;;
esac
BASE="${AGILIS_API_BASE:-https://ads.agilis.dating}"
BASE="${BASE%/}"

# ISO 8601 UTC, N minutes from now (GNU date or BSD/macOS date).
utc_in_minutes() {
  date -u -d "+$1 minutes" +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -v+"$1"M +%Y-%m-%dT%H:%M:%SZ
}

# A random UUID v4 for the Idempotency-Key (uuidgen, Linux, or /dev/urandom).
new_uuid() {
  if command -v uuidgen >/dev/null 2>&1; then uuidgen | tr 'A-Z' 'a-z'; return; fi
  if [ -r /proc/sys/kernel/random/uuid ]; then cat /proc/sys/kernel/random/uuid; return; fi
  local h; h=$(od -An -N16 -tx1 /dev/urandom | tr -d ' \n')
  printf '%s-%s-4%s-%x%s-%s\n' "${h:0:8}" "${h:8:4}" "${h:13:3}" $(( (0x${h:16:1} & 3) | 8 )) "${h:17:3}" "${h:20:12}"
}
