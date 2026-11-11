# Walkthrough: a Test Offer from start to finish

This uses curl and a Test key. Nothing is shown to members, and nothing is charged.

```bash
export AGILIS_API_KEY="pk_test_your_key_here"
```

## 1. Find a category

```bash
curl -sS "https://ads.agilis.dating/categories" -H "x-api-key: $AGILIS_API_KEY"
```

```json
{ "categories": [ { "category_id": 1, "category_name": "Retail" }, { "category_id": 2, "category_name": "Food & Beverage" } ] }
```

Your business can use the categories Agilis gave it when it was approved.

## 2. Check the price and the audience

```bash
curl -sS -X POST "https://ads.agilis.dating/offers/price-estimate" \
  -H "x-api-key: $AGILIS_API_KEY" -H "Content-Type: application/json" \
  -d '{"start_datetime":"2027-07-10T08:00:00Z","end_datetime":"2027-07-11T08:00:00Z","location":[51.5074,-0.1278],"radius":10,"environment":"TEST"}'
```

The response gives `matching_users` (members who used Agilis in the last 30 days and match your targeting), the `ad_units` (members × hours) and the `estimated_cost`. Dates must be now or later: change them to dates in the future.

## 3. Create the Offer

```bash
bash examples/curl/create-test-offer.sh 1 51.5074 -0.1278 10
```

The script sends a multipart request with the sample image, the location as two `location[]` fields, a start 5 minutes from now, an end 24 hours later and a new `Idempotency-Key`. A successful response:

```json
{ "return_code": "S1", "offer_id": 45, "status": "Awaiting Payment", "payment_url": "https://checkout.stripe.com/c/pay/cs_test_...", "currency": "GBP" }
```

- With `payment_method=E` (the default), open `payment_url` and pay with one of [Stripe's test cards](https://docs.stripe.com/testing). The Offer then becomes Active, or Scheduled if it starts later.
- With `PAYMENT_METHOD=B`, the cost comes from your Test balance, and the Offer is Active or Scheduled at once. If the balance is too low you get `E3`; top up your Test balance in the Ad Portal in Test mode.
- `E2`: the image was refused by automated moderation. Try another image.
- `E1` naming a minimum: a card payment below Stripe's minimum. Widen the audience, run the Offer longer, or pay from your balance.

## 4. See it in your list

```bash
bash examples/curl/list-offers.sh
```

## 5. Read its results

```bash
bash examples/curl/offer-analytics.sh 45 7d
```

```json
{ "offer_id": 45, "interval": "7d", "status": "Active", "metrics": { "views": 0, "clicks": 0 } }
```

Test Offers aren't shown to members, so their views and clicks stay at 0.

## 6. Pause, resume or delete

```bash
curl -sS -X POST "https://ads.agilis.dating/offers/45/pause"  -H "x-api-key: $AGILIS_API_KEY"
curl -sS -X POST "https://ads.agilis.dating/offers/45/resume" -H "x-api-key: $AGILIS_API_KEY"
curl -sS -X DELETE "https://ads.agilis.dating/offers/45"      -H "x-api-key: $AGILIS_API_KEY"
```

Test Offers are deleted automatically 30 days after they end.

## Events

Listing an Event works the same way: check `GET /event-config`, preview the image with `POST /events/preview`, then publish with `POST /events`. Events are paid from your balance. See the Events section of the [API reference](https://ads.agilis.dating/api-doc).
