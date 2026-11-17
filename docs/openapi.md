# OpenAPI description

The API is described in OpenAPI 3.1 at:

**https://www.agilis.dating/openapi.json**

It's generated from the same source as the [API reference](https://ads.agilis.dating/api-doc), so it's always current. This repository links to it rather than keeping a copy that could fall behind.

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
