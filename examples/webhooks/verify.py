# Verifies an Agilis webhook signature. Usage: AGILIS_WEBHOOK_SECRET=whsec_... AGILIS_SIGNATURE='t=...,v1=...' python verify.py body.json
import hashlib, hmac, json, time

# raw_body: the request body exactly as received (bytes), before any JSON parsing.
def verify_agilis_webhook(raw_body: bytes, header: str, secret: str, tolerance: int = 300) -> dict:
    parts = [p.strip().split("=", 1) for p in (header or "").split(",") if "=" in p]
    t = next((v for k, v in parts if k == "t"), "")
    signatures = [v for k, v in parts if k == "v1"]
    if not t.isdigit() or not signatures:
        raise ValueError("Invalid signature header")
    expected = hmac.new(secret.encode(), t.encode() + b"." + raw_body, hashlib.sha256).hexdigest()
    if not any(hmac.compare_digest(expected, s) for s in signatures):
        raise ValueError("Signature does not match")
    if abs(time.time() - int(t)) > tolerance:
        raise ValueError("Timestamp outside the tolerance")
    return json.loads(raw_body)


if __name__ == "__main__":
    import os, sys
    try:
        event = verify_agilis_webhook(open(sys.argv[1], "rb").read(), os.environ.get("AGILIS_SIGNATURE", ""), os.environ["AGILIS_WEBHOOK_SECRET"])
        print("verified " + event["type"])
    except ValueError as e:
        print("rejected: " + str(e), file=sys.stderr)
        sys.exit(1)
