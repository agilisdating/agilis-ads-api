import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.offers.list({
  limit: 20,
});
console.log(result.data?.length);
