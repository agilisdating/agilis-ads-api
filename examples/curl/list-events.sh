#!/usr/bin/env bash
# GET /events: your Test events. Pass a next_cursor as $1 for the next page.
source "$(dirname "$0")/_common.sh"
curl --fail-with-body -sS --retry 3 "$BASE/events?environment=test&limit=20${1:+&cursor=$1}" \
  -H "x-api-key: $AGILIS_API_KEY" \
  -H "Accept: application/json"
echo
