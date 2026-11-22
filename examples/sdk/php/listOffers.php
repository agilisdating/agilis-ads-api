<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->offers->list([
    'limit' => 20,
]);
echo count($result['data']), "\n";
