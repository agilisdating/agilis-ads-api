"""Build the Postman collection and Test environment from the Agilis OpenAPI description.

    python tools/build_postman.py                      # downloads https://www.agilis.dating/openapi.json
    python tools/build_postman.py path/to/openapi.json # or uses a local copy

Writes postman/agilis-ads-api.postman_collection.json and
postman/agilis-ads-api-test.postman_environment.json. Standard library only.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

SOURCE = "https://www.agilis.dating/openapi.json"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "postman"

# Requests that can charge money (a balance deduction or a payment link).
SPENDS = {"createOffer", "publishEvent"}


def load(src: str) -> dict:
    if re.match(r"^https?://", src):
        req = urllib.request.Request(src, headers={"User-Agent": "agilis-ads-api-examples/1.0", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    return json.loads(Path(src).read_text(encoding="utf-8"))


def example_value(name: str, schema: dict):
    schema = schema or {}
    if "example" in schema:
        return schema["example"]
    if "enum" in schema:
        values = schema["enum"]
        for preferred in ("test", "TEST"):
            if name == "environment" and preferred in values:
                return preferred
        return values[0]
    m = re.search(r"Example: `([^`]+)`", schema.get("description", ""))
    if m:
        text = m.group(1).strip()
        try:
            return json.loads(text)
        except ValueError:
            return text
    t = schema.get("type")
    if t == "integer":
        return schema.get("minimum", 1)
    if t == "number":
        return 0
    if t == "boolean":
        return False
    if t == "array":
        return []
    return ""


def text(v) -> str:
    return v if isinstance(v, str) else json.dumps(v)


def build_request(path: str, method: str, op: dict) -> dict:
    op_id = op.get("operationId", "")
    write = method in ("post", "patch", "put", "delete") and op_id != "estimateOfferPrice" and op_id != "previewEvent"
    marks = (" [write]" if write else "") + (" [spends]" if op_id in SPENDS else "")
    headers = [{"key": "x-api-key", "value": "{{api_key}}", "type": "text"}, {"key": "Accept", "value": "application/json", "type": "text"}]
    query, variables = [], []
    for p in op.get("parameters", []):
        value = example_value(p["name"], p.get("schema", {}))
        if p["in"] == "header":
            value = "{{$guid}}" if p["name"] == "Idempotency-Key" else text(value)
            headers.append({"key": p["name"], "value": value, "type": "text", "description": p.get("description", "")})
        elif p["in"] == "query":
            query.append({"key": p["name"], "value": text(value), "disabled": not p.get("required", False), "description": p.get("description", "")})
        elif p["in"] == "path":
            variables.append({"key": p["name"], "value": "", "description": p.get("description", "")})

    request = {
        "method": method.upper(),
        "header": headers,
        "url": {
            "raw": "{{base_url}}" + re.sub(r"\{(\w+)\}", r":\1", path) + ("?" + "&".join(f"{q['key']}={q['value']}" for q in query if not q["disabled"]) if any(not q["disabled"] for q in query) else ""),
            "host": ["{{base_url}}"],
            "path": [re.sub(r"\{(\w+)\}", r":\1", seg) for seg in path.strip("/").split("/")],
            "query": query,
            "variable": variables,
        },
        "description": (op.get("description") or op.get("summary") or "")
        + "\n\nReference: https://ads.agilis.dating/api-doc",
    }

    content = (op.get("requestBody") or {}).get("content", {})
    if "application/json" in content:
        props = content["application/json"].get("schema", {}).get("properties", {})
        body = {k: example_value(k, v) for k, v in props.items()}
        request["body"] = {"mode": "raw", "raw": json.dumps(body, indent=2), "options": {"raw": {"language": "json"}}}
    elif "multipart/form-data" in content:
        schema = content["multipart/form-data"].get("schema", {})
        required = set(schema.get("required", []))
        fields = []
        for k, v in schema.get("properties", {}).items():
            desc = v.get("description", "")
            if v.get("contentMediaType") or v.get("format") == "binary":
                fields.append({"key": k, "type": "file", "src": [], "description": desc, "disabled": k not in required})
                continue
            value = example_value(k, v)
            if v.get("type") == "array" or isinstance(value, list):
                items = value if isinstance(value, list) and value else [""]
                for item in items:
                    fields.append({"key": f"{k}[]", "value": text(item), "type": "text", "description": desc, "disabled": k not in required})
            else:
                fields.append({"key": k, "value": text(value), "type": "text", "description": desc, "disabled": k not in required})
        request["body"] = {"mode": "formdata", "formdata": fields}

    return {"name": (op.get("summary") or op_id) + marks, "request": request}


def main():
    spec = load(sys.argv[1] if len(sys.argv) > 1 else SOURCE)
    folders: dict = {}
    for path, methods in spec["paths"].items():
        for method, op in methods.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            tag = (op.get("tags") or ["Offers" if "offer" in path or path in ("/categories", "/interests") else "Events"])[0]
            folders.setdefault(tag, []).append(build_request(path, method, op))

    collection = {
        "info": {
            "name": "Agilis Advertising API",
            "description": (
                "Generated from https://www.agilis.dating/openapi.json by tools/build_postman.py "
                f"(OpenAPI {spec.get('info', {}).get('version', '')}).\n\n"
                "Use the Test environment and a Test key (pk_test_...). [write] requests change data; "
                "[spends] requests can charge money in Live mode. Reference: https://ads.agilis.dating/api-doc"
            ),
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "item": [{"name": name, "item": items} for name, items in folders.items()],
        "variable": [{"key": "base_url", "value": "https://ads.agilis.dating"}],
    }
    environment = {
        "name": "Agilis Advertising API: Test",
        "values": [
            {"key": "base_url", "value": "https://ads.agilis.dating", "type": "default", "enabled": True},
            {"key": "api_key", "value": "", "type": "secret", "enabled": True},
        ],
        "_postman_variable_scope": "environment",
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "agilis-ads-api.postman_collection.json").write_text(json.dumps(collection, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    (OUT / "agilis-ads-api-test.postman_environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"{sum(len(i) for i in folders.values())} requests in {len(folders)} folders")


if __name__ == "__main__":
    main()
