import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.webhookEndpoints.rollSecret('we_01JD2X4Q7N8P9R0S1T2V3W4X5Y', {
  expires_in: '24h',
});
console.log(result.secret);
