import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.events.edit(3104, {
  title: 'Thursday Comedy Club',
  url: 'https://www.barsalsa.co.uk/comedy',
  image: '/path/to/salsa.jpg',
});
console.log(result.status);
