# OpenAPI description

The API is described in OpenAPI 3.1 at:

**https://www.agilis.dating/openapi.json**

It's generated from the same source as the [API reference](https://www.agilis.dating/api-doc), so it's always current. [openapi/](../openapi) holds a copy, refreshed by a weekly job, so that every change to the contract is reviewed and checked for breaking changes.

Use it to:

- generate a client: for example `openapi-generator-cli generate -i https://www.agilis.dating/openapi.json -g python -o ./agilis-client`;
- import the API into Postman, Insomnia or Bruno;
- give an AI coding assistant the exact endpoints and fields.

If your HTTP client is refused when downloading the file, send a descriptive `User-Agent` header, for example `my-company-integration/1.0`.

The Postman collection in [postman/](../postman) is generated from this file by [tools/build_postman.py](../tools/build_postman.py).

## Lint rules

[`.spectral.yaml`](../.spectral.yaml) is the [Spectral](https://github.com/stoplightio/spectral) ruleset for the description. It extends Spectral's OpenAPI rules with ours, for example:

- one server, `https://ads.agilis.dating`, and the API key in the `x-api-key` header;
- kebab-case paths, snake_case parameters and verb-first `operationId`s;
- a summary, description, product tag and reference link on every operation;
- a documented `200` and `429` on every operation, and a bounded page size;
- an `Idempotency-Key` header on `POST /offers` and `POST /events`.

Rules marked `warn`, such as response schemas and examples, are being added to the description over time.

Lint it yourself:

```bash
npx @stoplight/spectral-cli lint --ruleset .spectral.yaml https://www.agilis.dating/openapi.json
```

## Other published files

| File | What it is |
|---|---|
| [/openapi/{offers,events,webhooks,reference}.json](https://www.agilis.dating/openapi/offers.json) | The same contract in parts |
| [/openapi/overlay.yaml](https://www.agilis.dating/openapi/overlay.yaml) | An [OpenAPI Overlay 1.0](https://spec.openapis.org/overlay/v1.0.0.html) with the logo, the tag groups and a request sample per language on each operation. Apply it with any Overlay tool, or with [tools/apply-overlay.mjs](../tools/apply-overlay.mjs) |
| [/schemas/offer.json](https://www.agilis.dating/schemas/offer.json) and `event`, `category`, `interest`, `page`, `error` | Each resource as a standalone JSON Schema 2020-12, the same as the OpenAPI components |
| [/context.jsonld](https://www.agilis.dating/context.jsonld) | A JSON-LD context that reads an Offer or an Event as schema.org data |
| [/asyncapi.json](https://www.agilis.dating/asyncapi.json) | The webhook messages, in AsyncAPI 3.0 |

## Contract checks

[.github/workflows/openapi-lint.yml](../.github/workflows/openapi-lint.yml) runs on every pull request, on main, and weekly:

- **Lint:** applies the overlay, then lints the contract, each part and the presented document with the ruleset.
- **Validate:** checks the AsyncAPI document and each JSON Schema.
- **Breaking changes:** on a pull request that changes `openapi/openapi.json`, checks it against main with [oasdiff](https://github.com/oasdiff/oasdiff). A breaking change fails unless the pull request has the label `breaking-change-approved`, which is added only with an entry in the public change log.
- **Refresh (weekly):** downloads the live contract and opens a pull request when it has changed.
