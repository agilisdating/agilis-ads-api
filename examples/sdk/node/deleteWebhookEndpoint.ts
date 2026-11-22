import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.webhookEndpoints.delete('we_01JD2X4Q7N8P9R0S1T2V3W4X5Y');
console.log(result.deleted);
