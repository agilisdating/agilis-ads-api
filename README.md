# Agilis Advertising API: examples

Examples for the **Agilis Advertising REST API**, by Agilis Dating Ltd.

Agilis is a dating app for adults who want to meet in person. Businesses that Agilis has approved can show **Offers** and list **Events** to nearby Agilis members in the Agilis apps and web app. They can do this in the [Agilis Ad Portal](https://adportal.agilis.dating), or from their own systems through this API.

This repository holds **documentation and examples only**: no application code, no keys, no member data. The API never returns information about individual members.

- **API reference:** https://ads.agilis.dating/api-doc
- **OpenAPI 3.1 description:** https://www.agilis.dating/openapi.json (see [docs/openapi.md](docs/openapi.md))
- **Advertiser's Guide:** https://www.agilis.dating/business/guide
- **Base URL:** `https://ads.agilis.dating`

## Before you start

1. **Your business must be approved.** Register at https://www.agilis.dating/business. We review every business, usually within 5 working days.
2. **Create a Test API key.** In the Ad Portal, switch to **Test mode**, open **Manage API Keys** and create a key. Test keys start with `pk_test_`. The key is shown once; **Roll key** replaces a lost one.
3. **Keep the key secret.** Put it in an environment variable, never in code or in this repository.

In Test mode nothing is shown to members and nothing is charged. Test Offers and Events are deleted 30 days after they end. Every example here refuses to run with a Live key (`pk_live_`).

## Quick start (curl)

```bash
export AGILIS_API_KEY="pk_test_your_key_here"

curl "https://ads.agilis.dating/offers?environment=test" \
  -H "x-api-key: $AGILIS_API_KEY"
```

A successful response looks like:

```json
{
  "data": [],
  "pagination": { "limit": 20, "count": 0, "has_more": false, "next_cursor": null }
}
```

## Examples

Each example does the same four things:

| Task | Endpoint |
|---|---|
| List your Offers | `GET /offers?environment=test` |
| Create a Test Offer with an image | `POST /offers` (multipart, with an `Idempotency-Key`) |
| List your Events | `GET /events?environment=test` |
| Get an Offer's results | `GET /offers/{offer_id}/analytics?interval=7d` |

| Language | Where | Run |
|---|---|---|
| curl | [examples/curl](examples/curl) | `bash examples/curl/list-offers.sh` |
| Python 3.9+ (`requests`) | [examples/python](examples/python) | `python examples/python/agilis_examples.py list-offers` |
| Node.js 20+ (built-in `fetch`) | [examples/node](examples/node) | `node examples/node/agilis-examples.mjs list-offers` |
| PHP 8.1+ (curl extension) | [examples/php](examples/php) | `php examples/php/agilis-examples.php list-offers` |

All of them read `AGILIS_API_KEY` (and optionally `AGILIS_API_BASE`) from the environment. Copy [.env.example](.env.example) if you use a `.env` loader.

A step-by-step Test Offer, from finding a category to reading its results, is in [docs/walkthrough-offer.md](docs/walkthrough-offer.md).

## Postman

Import [postman/agilis-ads-api.postman_collection.json](postman/agilis-ads-api.postman_collection.json) and the Test environment [postman/agilis-ads-api-test.postman_environment.json](postman/agilis-ads-api-test.postman_environment.json), then set `api_key` to your Test key. Requests that create something or can spend money are marked **[write]** and **[spends]**. The collection is generated from the OpenAPI description by [tools/build_postman.py](tools/build_postman.py).

## Authentication, limits and errors

- Send your key in the `x-api-key` header on every request.
- **60 requests a minute per API key**, across every endpoint, uploads included. Over the limit you get HTTP `429` with a `Retry-After` header: wait that many seconds.
- Any wrong, expired or disabled key gets the same HTTP `401` `{"message": "Unauthorised"}`. Repeated wrong keys from one IP address are blocked for a while.
- `environment` must match your key's mode: a `pk_test_` key works with `environment=test` / `TEST` only.
- `POST /offers` and `POST /events` need an `Idempotency-Key` header. Retrying with the same key never creates a duplicate or a second payment.

More in [docs/errors.md](docs/errors.md).

## Support

- Questions about the API or your account: help@agilis.dating
- Security issues: see [SECURITY.md](SECURITY.md)

## Licence

The examples are released under the [MIT Licence](LICENSE). "Agilis" and the Agilis logo are trade marks of Agilis Dating Ltd and aren't covered by the licence.
