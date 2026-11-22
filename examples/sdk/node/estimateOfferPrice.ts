import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.offers.estimatePrice({
  start_datetime: '2027-07-10T08:00:00Z',
  end_datetime: '2027-07-12T20:30:00Z',
  location: [51.5074, -0.1278],
  radius: 10,
  gender: ['Male', 'Female'],
  interests: [3, 7],
});
console.log(result.estimated_cost);
