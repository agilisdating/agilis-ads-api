#!/usr/bin/env bash
# POST /offers: a Test offer with an image.
#   bash create-test-offer.sh <category_id> <latitude> <longitude> [radius_miles] [image]
# Prints the Idempotency-Key it used: rerun with IDEMPOTENCY_KEY=<that key> to retry safely.
source "$(dirname "$0")/_common.sh"
CATEGORY="${1:?category_id from GET /categories}"
LAT="${2:?latitude}"
LNG="${3:?longitude}"
RADIUS="${4:-10}"
IMAGE="${5:-$(dirname "$0")/../assets/sample-offer.png}"
KEY="${IDEMPOTENCY_KEY:-$(new_uuid)}"
echo "Idempotency-Key: $KEY" >&2

# Some refusals are HTTP 200 with an E return_code (for example E2: image refused): read return_code.
# payment_method E = a Stripe test-mode payment link; B = your Test balance.
curl --fail-with-body -sS --retry 3 -X POST "$BASE/offers" \
  -H "x-api-key: $AGILIS_API_KEY" \
  -H "Accept: application/json" \
  -H "Idempotency-Key: $KEY" \
  -F "environment=TEST" \
  -F "category_id=$CATEGORY" \
  -F "title=2-for-1 cocktails before 8pm" \
  -F "description=Show this offer at the bar to get your second cocktail free." \
  -F "terms_and_conditions=One per person. Test offer created by the API examples." \
  -F "push_notification_title=2-for-1 cocktails tonight" \
  -F "push_notification_message=Show this at the bar before 8pm for a free second cocktail." \
  -F "button_preset=book_now" \
  -F "url=https://www.example.com/offer" \
  -F "location[]=$LAT" \
  -F "location[]=$LNG" \
  -F "radius=$RADIUS" \
  -F "start_datetime=$(utc_in_minutes 5)" \
  -F "expiry_datetime=$(utc_in_minutes 1445)" \
  -F "payment_method=${PAYMENT_METHOD:-E}" \
  -F "image=@$IMAGE"
echo
