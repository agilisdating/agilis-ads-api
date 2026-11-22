<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->events->preview([
    'title' => 'Beginners Cuban Salsa: Friday Social',
    'description' => 'Drop-in class for absolute beginners, followed by a social until late. No partner needed.',
    'venue_name' => 'Bar Salsa',
    'address' => '96 Charing Cross Road',
    'city' => 'London',
    'country_code' => 'GB',
    'location' => [51.5133, -0.1300],
    'starts_at' => '2027-10-16T18:30:00Z',
    'ends_at' => '2027-10-16T23:00:00Z',
    'url' => 'https://www.barsalsa.co.uk/classes/friday',
    'price_min' => 12,
    'price_max' => 12,
    'currency' => 'GBP',
    'image' => '/path/to/salsa.jpg',
]);
echo $result['balance_after'], "\n";
