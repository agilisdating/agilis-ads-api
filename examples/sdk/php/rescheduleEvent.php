<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->events->reschedule(3104, [
    'starts_at' => '2027-10-23T18:30:00Z',
    'ends_at' => '2027-10-23T23:00:00Z',
]);
echo $result['status'], "\n";
