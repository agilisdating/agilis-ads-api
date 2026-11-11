#!/usr/bin/env bash
# GET /offers/{offer_id}/analytics: views and clicks.
#   bash offer-analytics.sh <offer_id> [24h|7d|30d|60d|90d|all]
source "$(dirname "$0")/_common.sh"
OFFER="${1:?offer_id}"
curl --fail-with-body -sS --retry 3 "$BASE/offers/$OFFER/analytics?interval=${2:-7d}" \
  -H "x-api-key: $AGILIS_API_KEY" \
  -H "Accept: application/json"
echo
