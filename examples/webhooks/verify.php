<?php
// Verifies an Agilis webhook signature. Usage: AGILIS_WEBHOOK_SECRET=whsec_... AGILIS_SIGNATURE='t=...,v1=...' php verify.php body.json
// $rawBody: the request body exactly as received, e.g. file_get_contents('php://input').
function verifyAgilisWebhook(string $rawBody, string $header, string $secret, int $tolerance = 300): array
{
    $t = null;
    $signatures = [];
    foreach (explode(',', $header) as $part) {
        [$k, $v] = array_pad(explode('=', trim($part), 2), 2, '');
        if ($k === 't') { $t = $v; }
        if ($k === 'v1') { $signatures[] = $v; }
    }
    if ($t === null || !ctype_digit($t) || $signatures === []) {
        throw new RuntimeException('Invalid signature header');
    }
    $expected = hash_hmac('sha256', $t . '.' . $rawBody, $secret);
    $ok = false;
    foreach ($signatures as $s) { $ok = $ok || hash_equals($expected, $s); }
    if (!$ok) { throw new RuntimeException('Signature does not match'); }
    if (abs(time() - (int) $t) > $tolerance) { throw new RuntimeException('Timestamp outside the tolerance'); }
    return json_decode($rawBody, true, 512, JSON_THROW_ON_ERROR);
}

try {
    $event = verifyAgilisWebhook(file_get_contents($argv[1]), (string) getenv('AGILIS_SIGNATURE'), (string) getenv('AGILIS_WEBHOOK_SECRET'));
    echo 'verified ' . $event['type'] . PHP_EOL;
} catch (RuntimeException $e) {
    fwrite(STDERR, 'rejected: ' . $e->getMessage() . PHP_EOL);
    exit(1);
}
