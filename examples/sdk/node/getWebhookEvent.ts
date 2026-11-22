import { Agilis } from '@agilisdating/ads';

const client = new Agilis(); // reads AGILIS_API_KEY

const result = await client.webhookEvents.get('whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M');
console.log(result.type);
