<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->webhookEndpoints->sendTest('we_01JD2X4Q7N8P9R0S1T2V3W4X5Y', [
    'type' => 'offer.started',
]);
echo $result['webhook_event_id'], "\n";
