#!/usr/bin/env bash
# Downloads the published contract into openapi/: the OpenAPI description (whole and in parts),
# the presentation overlay, the AsyncAPI document, each resource's JSON Schema and the JSON-LD
# context. Run by the contract workflow; run it yourself to refresh the copy.
set -euo pipefail

SITE="https://www.agilis.dating"
UA="agilis-ads-api-contract/1.0 (+https://github.com/agilisdating/agilis-ads-api)"
get() { curl --fail --silent --show-error --location --user-agent "$UA" --output "$2" "$SITE/$1"; }

mkdir -p openapi/parts openapi/schemas
get openapi.json openapi/openapi.json
for part in offers events webhooks reference; do get "openapi/$part.json" "openapi/parts/$part.json"; done
get openapi/overlay.yaml openapi/overlay.yaml
get asyncapi.json openapi/asyncapi.json
for schema in offer event category interest page error; do get "schemas/$schema.json" "openapi/schemas/$schema.json"; done
get context.jsonld openapi/context.jsonld
