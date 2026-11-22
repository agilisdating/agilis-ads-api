// Verifies an Agilis webhook signature. Usage: AGILIS_WEBHOOK_SECRET=whsec_... AGILIS_SIGNATURE='t=...,v1=...' node verify.js body.json
const crypto = require('node:crypto');

// rawBody: the request body exactly as received (a Buffer or string), before any JSON parsing.
function verifyAgilisWebhook(rawBody, header, secret, toleranceSeconds = 300) {
  const parts = String(header || '').split(',').map((p) => p.trim().split('='));
  const t = (parts.find(([k]) => k === 't') || [])[1];
  const signatures = parts.filter(([k]) => k === 'v1').map(([, v]) => v);
  if (!/^\d+$/.test(t || '') || signatures.length === 0) throw new Error('Invalid signature header');
  const expected = crypto.createHmac('sha256', secret).update(`${t}.${rawBody}`).digest('hex');
  const ok = signatures.some((s) => s.length === expected.length
    && crypto.timingSafeEqual(Buffer.from(s), Buffer.from(expected)));
  if (!ok) throw new Error('Signature does not match');
  if (Math.abs(Date.now() / 1000 - Number(t)) > toleranceSeconds) throw new Error('Timestamp outside the tolerance');
  return JSON.parse(rawBody);
}

const fs = require('node:fs');
try {
  const event = verifyAgilisWebhook(fs.readFileSync(process.argv[2], 'utf8'), process.env.AGILIS_SIGNATURE, process.env.AGILIS_WEBHOOK_SECRET);
  console.log(`verified ${event.type}`);
} catch (e) {
  console.error(`rejected: ${e.message}`);
  process.exit(1);
}
