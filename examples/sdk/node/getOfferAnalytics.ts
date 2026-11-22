import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.offers.analytics(45, { interval: '30d' });
console.log(result.status);
