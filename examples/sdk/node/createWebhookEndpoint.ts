import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.webhookEndpoints.create({
  url: 'https://hooks.example.com/agilis',
  enabled_events: ['offer.started', 'offer.ended', 'event.published'],
  description: 'Order system',
});
console.log(result.secret);
