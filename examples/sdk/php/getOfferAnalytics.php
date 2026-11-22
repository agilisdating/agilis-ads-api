<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->offers->analytics(45, ['interval' => '30d']);
echo $result['status'], "\n";
