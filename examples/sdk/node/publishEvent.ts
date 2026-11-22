import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

// An Idempotency-Key is sent for you, and reused if the request is retried.
const result = await client.events.publish({
  title: 'Beginners Cuban Salsa: Friday Social',
  description: 'Drop-in class for absolute beginners, followed by a social until late. No partner needed.',
  venue_name: 'Bar Salsa',
  address: '96 Charing Cross Road',
  city: 'London',
  country_code: 'GB',
  location: [51.5133, -0.1300],
  starts_at: '2027-10-16T18:30:00Z',
  ends_at: '2027-10-16T23:00:00Z',
  url: 'https://www.barsalsa.co.uk/classes/friday',
  price_min: 12,
  price_max: 12,
  currency: 'GBP',
  payment_method: 'B',
  preview_token: 'evp_8f3c1a…',
});
console.log(result.event_id);
