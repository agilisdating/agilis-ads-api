<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->webhookEndpoints->create([
    'url' => 'https://hooks.example.com/agilis',
    'enabled_events' => ['offer.started', 'offer.ended', 'event.published'],
    'description' => 'Order system',
]);
echo $result['secret'], "\n";
