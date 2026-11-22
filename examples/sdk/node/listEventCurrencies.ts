import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.eventCurrencies.list();
console.log(result.currencies?.length);
