<?php

require 'vendor/autoload.php';

use Agilis\Ads\AgilisClient;

$agilis = new AgilisClient(); // reads AGILIS_API_KEY

$result = $agilis->webhookEndpoints->get('we_01JD2X4Q7N8P9R0S1T2V3W4X5Y');
echo $result['status'], "\n";
