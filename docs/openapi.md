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
