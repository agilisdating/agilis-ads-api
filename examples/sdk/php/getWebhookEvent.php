<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->webhookEvents->get('whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M');
echo $result['type'], "\n";
