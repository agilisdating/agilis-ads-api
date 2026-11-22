import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.webhookEndpoints.sendTest('we_01JD2X4Q7N8P9R0S1T2V3W4X5Y', {
  type: 'offer.started',
});
console.log(result.webhook_event_id);
