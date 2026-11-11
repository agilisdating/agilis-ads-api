# Errors, limits and retries

The full list of return codes for every endpoint is in the [API reference](https://ads.agilis.dating/api-doc). This page covers what every client needs to handle.

## Read both the HTTP status and `return_code`

Most responses carry a `return_code`: `S1`, `S2` and so on for success, `E1`, `E2` and so on for a refusal, with a `message`.

**Some refusals are HTTP 200.** For example, `POST /offers` returns HTTP 200 with:

- `E2`: the image failed automated content moderation. Nothing was created. Choose a different image.
- `E3`: your balance is less than the offer's cost (`payment_method=B` only). Top up and retry.

So check `return_code`, not just the status. The examples in this repository treat any `E…` code as a failure.

The meaning of a code depends on the endpoint: `E2` on `POST /offers` isn't `E2` on `POST /offers/{offer_id}/pause`. Look codes up per endpoint.

## Authentication: 401 and 403

| Response | Meaning |
|---|---|
| `401` `{"status": false, "message": "API key missing"}` | No `x-api-key` header. |
| `401` `{"message": "Unauthorised"}` | The key is wrong, expired or disabled, or its organisation can't use the API. The response is the same in every case, on purpose. |
| `403` with `return_code` `E1` | `environment` isn't your key's mode, for example `environment=live` with a `pk_test_` key. |

## Rate limits: 429 and `Retry-After`

- **60 requests a minute per API key**, across every endpoint, uploads included.
- Responses carry `X-RateLimit-Limit` and `X-RateLimit-Remaining`.
- Over the limit you get HTTP `429` and a `Retry-After` header: the number of seconds to wait. Wait that long, then retry.
- Too many requests with **wrong** keys from one IP address are refused with `429` for a while, whatever key is sent next.
- `POST /events/preview` has its own limit of 60 previews per organisation per hour (`E8`, HTTP 429).

## Retrying safely: `Idempotency-Key`

`POST /offers` and `POST /events` need an `Idempotency-Key` header: a unique value you create for each new Offer or Event, such as a UUID v4.

- If a request times out, or you get a `429` or `5xx`, retry with **the same** `Idempotency-Key` and the same body. You get the original response back, with no second Offer, Event or payment.
- `409`: the first request with that key is still being processed. Retry shortly.
- `422`: the key was already used with a different body. Use a new key for a different Offer.
- A missing key gets HTTP `400` `E1`: "Idempotency-Key header is required."

## Test and Live

A `pk_test_` key works only in Test mode (`environment=test` / `TEST`), and a `pk_live_` key only in Live. Test and Live balances are separate. In Test mode, nothing is shown to members and nothing is charged. Card payments go through Stripe's test mode, and Test Offers and Events are deleted 30 days after they end.
