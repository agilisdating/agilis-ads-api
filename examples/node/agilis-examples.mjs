// Agilis Advertising API examples (Node.js 20+, no dependencies).
//
//   export AGILIS_API_KEY="pk_test_..."        # a Test key from the Ad Portal
//   node agilis-examples.mjs list-offers
//   node agilis-examples.mjs estimate --lat=51.5074 --lng=-0.1278 --radius=10
//   node agilis-examples.mjs create-offer --category=1 --lat=51.5074 --lng=-0.1278 --radius=10
//   node agilis-examples.mjs list-events
//   node agilis-examples.mjs analytics --offer 45 --interval 7d
//
// Test mode only: every command refuses a Live key (pk_live_).
// Write negative numbers as --lng=-0.1278 (with =), so they aren't read as an option.
// API reference: https://ads.agilis.dating/api-doc

import { openAsBlob } from "node:fs";
import { basename, dirname, extname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { randomUUID } from "node:crypto";
import { parseArgs } from "node:util";

const BASE = (process.env.AGILIS_API_BASE || "https://ads.agilis.dating").replace(/\/+$/, "");
const SAMPLE_IMAGE = join(dirname(fileURLToPath(import.meta.url)), "..", "assets", "sample-offer.png");

function apiKey() {
  const key = (process.env.AGILIS_API_KEY || "").trim();
  if (!key) fail("Set AGILIS_API_KEY to your Test API key (pk_test_...).");
  if (!key.startsWith("pk_test_")) fail("These examples run in Test mode only: use a key that starts with pk_test_.");
  return key;
}

function fail(message) {
  console.error(message);
  process.exit(1);
}

const iso = (date) => date.toISOString().replace(/\.\d{3}Z$/, "Z");

// One request, waiting and retrying when the API answers 429 (rate limit).
async function call(method, path, { query, json, form, headers = {} } = {}, retries = 3) {
  const url = new URL(BASE + path);
  for (const [k, v] of Object.entries(query || {})) if (v !== undefined) url.searchParams.set(k, String(v));
  for (let attempt = 0; ; attempt++) {
    const init = { method, headers: { "x-api-key": apiKey(), Accept: "application/json", ...headers } };
    if (json) {
      init.headers["Content-Type"] = "application/json";
      init.body = JSON.stringify(json);
    } else if (form) {
      init.body = await form(); // a fresh FormData each attempt
    }
    const response = await fetch(url, init);
    if (response.status !== 429 || attempt >= retries) return response;
    const wait = Number(response.headers.get("Retry-After") || 5);
    console.error(`Rate limited: waiting ${wait} s (attempt ${attempt + 1}/${retries})`);
    await new Promise((resolve) => setTimeout(resolve, wait * 1000));
  }
}

async function show(response) {
  const text = await response.text();
  let body;
  try { body = JSON.parse(text); } catch { body = { raw: text }; }
  console.log(`HTTP ${response.status}`);
  console.log(JSON.stringify(body, null, 2));
  // Some refusals are HTTP 200 with an E return_code (for example E2: image refused): check both.
  if (response.status >= 400 || String(body.return_code || "").startsWith("E")) process.exit(1);
  return body;
}

const commands = {
  async "list-offers"(o) {
    await show(await call("GET", "/offers", { query: { environment: "test", limit: o.limit || 20, cursor: o.cursor } }));
  },

  async estimate(o) {
    need(o, ["lat", "lng"]);
    const start = new Date(Date.now() + 5 * 60_000);
    await show(await call("POST", "/offers/price-estimate", {
      json: {
        start_datetime: iso(start),
        end_datetime: iso(new Date(start.getTime() + Number(o.hours || 24) * 3_600_000)),
        location: [Number(o.lat), Number(o.lng)],
        radius: Number(o.radius || 10),
        environment: "TEST",
      },
    }));
  },

  async "create-offer"(o) {
    need(o, ["category", "lat", "lng"]);
    const start = new Date(Date.now() + 5 * 60_000);
    const image = o.image || SAMPLE_IMAGE;
    const type = extname(image).toLowerCase() === ".png" ? "image/png" : "image/jpeg";
    // One Idempotency-Key per offer: a retry with the same key never creates a second offer or payment.
    const idempotencyKey = o["idempotency-key"] || randomUUID();
    console.error(`Idempotency-Key: ${idempotencyKey}`);
    const fields = [
      ["environment", "TEST"],
      ["category_id", String(o.category)],
      ["title", "2-for-1 cocktails before 8pm"],
      ["description", "Show this offer at the bar to get your second cocktail free."],
      ["terms_and_conditions", "One per person. Test offer created by the API examples."],
      ["push_notification_title", "2-for-1 cocktails tonight"],
      ["push_notification_message", "Show this at the bar before 8pm for a free second cocktail."],
      ["button_preset", "book_now"],
      ["url", o.url || "https://www.example.com/offer"],
      ["location[]", String(o.lat)],
      ["location[]", String(o.lng)],
      ["radius", String(o.radius || 10)],
      ["start_datetime", iso(start)],
      ["expiry_datetime", iso(new Date(start.getTime() + Number(o.hours || 24) * 3_600_000))],
      ["payment_method", o["payment-method"] || "E"], // E: Stripe test-mode link; B: your Test balance
    ];
    const form = async () => {
      const fd = new FormData();
      for (const [k, v] of fields) fd.append(k, v);
      fd.append("image", await openAsBlob(image, { type }), basename(image));
      return fd;
    };
    await show(await call("POST", "/offers", { form, headers: { "Idempotency-Key": idempotencyKey } }));
  },

  async "list-events"(o) {
    await show(await call("GET", "/events", { query: { environment: "test", limit: o.limit || 20, cursor: o.cursor } }));
  },

  async analytics(o) {
    need(o, ["offer"]);
    await show(await call("GET", `/offers/${encodeURIComponent(o.offer)}/analytics`, { query: { interval: o.interval || "7d" } }));
  },
};

function need(o, names) {
  for (const n of names) if (o[n] === undefined) fail(`--${n} is required.`);
}

const [command, ...rest] = process.argv.slice(2);
if (!commands[command]) fail(`Usage: node agilis-examples.mjs <${Object.keys(commands).join("|")}> [options]`);
const { values } = parseArgs({
  args: rest,
  options: Object.fromEntries(
    ["limit", "cursor", "lat", "lng", "radius", "hours", "category", "url", "image", "payment-method", "idempotency-key", "offer", "interval"]
      .map((n) => [n, { type: "string" }]),
  ),
});
await commands[command](values);
