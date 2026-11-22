import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.interests.list();
console.log(result.interests?.length);
