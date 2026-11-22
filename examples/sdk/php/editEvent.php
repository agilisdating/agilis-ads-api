<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->events->edit(3104, [
    'title' => 'Thursday Comedy Club',
    'url' => 'https://www.barsalsa.co.uk/comedy',
    'image' => '/path/to/salsa.jpg',
]);
echo $result['status'], "\n";
