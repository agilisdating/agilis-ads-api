#!/usr/bin/env bash
# GET /offers: your Test offers, newest first. Pass a next_cursor as $1 for the next page.
source "$(dirname "$0")/_common.sh"
curl --fail-with-body -sS --retry 3 "$BASE/offers?environment=test&limit=20${1:+&cursor=$1}" \
  -H "x-api-key: $AGILIS_API_KEY" \
  -H "Accept: application/json"
echo
