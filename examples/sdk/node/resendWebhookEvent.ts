import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.webhookEvents.resend('whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M', {
  endpoint_id: 'we_01JD2X4Q7N8P9R0S1T2V3W4X5Y',
});
console.log(result.webhook_event_id);
