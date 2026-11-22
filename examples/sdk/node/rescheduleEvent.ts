import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.events.reschedule(3104, {
  starts_at: '2027-10-23T18:30:00Z',
  ends_at: '2027-10-23T23:00:00Z',
});
console.log(result.status);
