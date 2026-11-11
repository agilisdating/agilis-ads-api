"""Agilis Advertising API examples (Python 3.9+, `pip install requests`).

    export AGILIS_API_KEY="pk_test_..."        # a Test key from the Ad Portal
    python agilis_examples.py list-offers
    python agilis_examples.py estimate --lat 51.5074 --lng=-0.1278 --radius 10
    python agilis_examples.py create-offer --category 1 --lat 51.5074 --lng=-0.1278 --radius 10
    python agilis_examples.py list-events
    python agilis_examples.py analytics --offer 45 --interval 7d

Test mode only: every command refuses a Live key (pk_live_).
API reference: https://ads.agilis.dating/api-doc
"""
import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

BASE = os.environ.get("AGILIS_API_BASE", "https://ads.agilis.dating").rstrip("/")
SAMPLE_IMAGE = Path(__file__).resolve().parent.parent / "assets" / "sample-offer.png"


def api_key() -> str:
    key = os.environ.get("AGILIS_API_KEY", "").strip()
    if not key:
        sys.exit("Set AGILIS_API_KEY to your Test API key (pk_test_...).")
    if not key.startswith("pk_test_"):
        sys.exit("These examples run in Test mode only: use a key that starts with pk_test_.")
    return key


def call(method: str, path: str, *, retries: int = 3, **kwargs) -> requests.Response:
    """One request, waiting and retrying when the API answers 429 (rate limit)."""
    headers = {"x-api-key": api_key(), "Accept": "application/json", **kwargs.pop("headers", {})}
    for attempt in range(retries + 1):
        response = requests.request(method, BASE + path, headers=headers, timeout=60, **kwargs)
        if response.status_code != 429 or attempt == retries:
            return response
        wait = int(response.headers.get("Retry-After", "5"))
        print(f"Rate limited: waiting {wait} s (attempt {attempt + 1}/{retries})", file=sys.stderr)
        time.sleep(wait)
    return response


def show(response: requests.Response) -> dict:
    try:
        body = response.json()
    except ValueError:
        body = {"raw": response.text}
    print(f"HTTP {response.status_code}")
    print(json.dumps(body, indent=2, ensure_ascii=False))
    # Some refusals are HTTP 200 with an E return_code (for example E2: image refused): check both.
    code = body.get("return_code") if isinstance(body, dict) else None
    if response.status_code >= 400 or (code and code.startswith("E")):
        sys.exit(1)
    return body


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def list_offers(args):
    params = {"environment": "test", "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    show(call("GET", "/offers", params=params))


def estimate(args):
    start = datetime.now(timezone.utc) + timedelta(minutes=5)
    payload = {
        "start_datetime": iso(start),
        "end_datetime": iso(start + timedelta(hours=args.hours)),
        "location": [args.lat, args.lng],
        "radius": args.radius,
        "environment": "TEST",
    }
    show(call("POST", "/offers/price-estimate", json=payload))


def create_offer(args):
    start = datetime.now(timezone.utc) + timedelta(minutes=5)
    form = [
        ("environment", "TEST"),
        ("category_id", str(args.category)),
        ("title", "2-for-1 cocktails before 8pm"),
        ("description", "Show this offer at the bar to get your second cocktail free."),
        ("terms_and_conditions", "One per person. Test offer created by the API examples."),
        ("push_notification_title", "2-for-1 cocktails tonight"),
        ("push_notification_message", "Show this at the bar before 8pm for a free second cocktail."),
        ("button_preset", "book_now"),
        ("url", args.url),
        ("location[]", str(args.lat)),
        ("location[]", str(args.lng)),
        ("radius", str(args.radius)),
        ("start_datetime", iso(start)),
        ("expiry_datetime", iso(start + timedelta(hours=args.hours))),
        ("payment_method", args.payment_method),
    ]
    image = Path(args.image)
    # One Idempotency-Key per offer: a retry with the same key never creates a second offer or payment.
    idempotency_key = args.idempotency_key or str(uuid.uuid4())
    print(f"Idempotency-Key: {idempotency_key}", file=sys.stderr)
    with image.open("rb") as fh:
        files = {"image": (image.name, fh, "image/png" if image.suffix.lower() == ".png" else "image/jpeg")}
        response = call("POST", "/offers", data=form, files=files, headers={"Idempotency-Key": idempotency_key})
    show(response)


def list_events(args):
    params = {"environment": "test", "limit": args.limit}
    if args.cursor:
        params["cursor"] = args.cursor
    show(call("GET", "/events", params=params))


def analytics(args):
    show(call("GET", f"/offers/{args.offer}/analytics", params={"interval": args.interval}))


def main():
    parser = argparse.ArgumentParser(description="Agilis Advertising API examples (Test mode)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("list-offers", help="GET /offers")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--cursor")
    p.set_defaults(func=list_offers)

    p = sub.add_parser("estimate", help="POST /offers/price-estimate")
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lng", type=float, required=True)
    p.add_argument("--radius", type=int, default=10, help="5 to 30 miles")
    p.add_argument("--hours", type=int, default=24)
    p.set_defaults(func=estimate)

    p = sub.add_parser("create-offer", help="POST /offers with an image")
    p.add_argument("--category", type=int, required=True, help="an id from GET /categories")
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lng", type=float, required=True)
    p.add_argument("--radius", type=int, default=10, help="5 to 30 miles")
    p.add_argument("--hours", type=int, default=24)
    p.add_argument("--url", default="https://www.example.com/offer")
    p.add_argument("--image", default=str(SAMPLE_IMAGE), help="JPG, PNG or GIF, up to 5 MB")
    p.add_argument("--payment-method", choices=["E", "B"], default="E",
                   help="E: a Stripe test-mode payment link (default); B: your Test balance")
    p.add_argument("--idempotency-key", help="reuse to retry the same offer safely")
    p.set_defaults(func=create_offer)

    p = sub.add_parser("list-events", help="GET /events")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--cursor")
    p.set_defaults(func=list_events)

    p = sub.add_parser("analytics", help="GET /offers/{offer_id}/analytics")
    p.add_argument("--offer", type=int, required=True)
    p.add_argument("--interval", default="7d", choices=["24h", "7d", "30d", "60d", "90d", "all"])
    p.set_defaults(func=analytics)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
