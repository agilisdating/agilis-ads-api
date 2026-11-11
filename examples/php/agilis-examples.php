<?php
/**
 * Agilis Advertising API examples (PHP 8.1+, curl extension).
 *
 *   export AGILIS_API_KEY="pk_test_..."        # a Test key from the Ad Portal
 *   php agilis-examples.php list-offers
 *   php agilis-examples.php estimate --lat=51.5074 --lng=-0.1278 --radius=10
 *   php agilis-examples.php create-offer --category=1 --lat=51.5074 --lng=-0.1278 --radius=10
 *   php agilis-examples.php list-events
 *   php agilis-examples.php analytics --offer=45 --interval=7d
 *
 * Test mode only: every command refuses a Live key (pk_live_).
 * API reference: https://ads.agilis.dating/api-doc
 */

declare(strict_types=1);

const SAMPLE_IMAGE = __DIR__ . '/../assets/sample-offer.png';

function fail(string $message): never
{
    fwrite(STDERR, $message . PHP_EOL);
    exit(1);
}

function base(): string
{
    return rtrim(getenv('AGILIS_API_BASE') ?: 'https://ads.agilis.dating', '/');
}

function apiKey(): string
{
    $key = trim((string) getenv('AGILIS_API_KEY'));
    if ($key === '') {
        fail('Set AGILIS_API_KEY to your Test API key (pk_test_...).');
    }
    if (!str_starts_with($key, 'pk_test_')) {
        fail('These examples run in Test mode only: use a key that starts with pk_test_.');
    }
    return $key;
}

function iso(DateTimeImmutable $t): string
{
    return $t->setTimezone(new DateTimeZone('UTC'))->format('Y-m-d\TH:i:s\Z');
}

/**
 * One request, waiting and retrying when the API answers 429 (rate limit).
 * $body: array for JSON, string for an already-encoded multipart/form body, or null.
 *
 * @return array{0:int,1:array<string,string>,2:string}
 */
function call(string $method, string $path, array $query = [], array|string|null $body = null, array $headers = [], int $retries = 3): array
{
    $url = base() . $path . ($query ? '?' . http_build_query($query) : '');
    for ($attempt = 0; ; $attempt++) {
        $h = ['x-api-key: ' . apiKey(), 'Accept: application/json'];
        foreach ($headers as $k => $v) {
            $h[] = $k . ': ' . $v;
        }
        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_TIMEOUT, 60);
        if (is_array($body)) {
            $h[] = 'Content-Type: application/json';
            curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($body));
        } elseif (is_string($body)) {
            curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
        }
        curl_setopt($ch, CURLOPT_HTTPHEADER, $h);
        $responseHeaders = [];
        curl_setopt($ch, CURLOPT_HEADERFUNCTION, function ($ch, string $line) use (&$responseHeaders) {
            $parts = explode(':', $line, 2);
            if (count($parts) === 2) {
                $responseHeaders[strtolower(trim($parts[0]))] = trim($parts[1]);
            }
            return strlen($line);
        });
        $text = curl_exec($ch);
        if ($text === false) {
            fail('Request failed: ' . curl_error($ch));
        }
        $status = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        if ($status !== 429 || $attempt >= $retries) {
            return [$status, $responseHeaders, (string) $text];
        }
        $wait = (int) ($responseHeaders['retry-after'] ?? 5);
        fwrite(STDERR, "Rate limited: waiting {$wait} s (attempt " . ($attempt + 1) . "/{$retries})" . PHP_EOL);
        sleep($wait);
    }
}

/**
 * multipart/form-data with repeated fields (location[]) and one file. Built by hand
 * so the same bytes can be resent unchanged on a retry.
 *
 * @param list<array{0:string,1:string}> $fields
 * @return array{0:string,1:string} [body, content type]
 */
function multipart(array $fields, string $fileField, string $path): array
{
    $boundary = 'agilis' . bin2hex(random_bytes(12));
    $out = '';
    foreach ($fields as [$name, $value]) {
        $out .= "--{$boundary}\r\nContent-Disposition: form-data; name=\"{$name}\"\r\n\r\n{$value}\r\n";
    }
    $type = strtolower(pathinfo($path, PATHINFO_EXTENSION)) === 'png' ? 'image/png' : 'image/jpeg';
    $out .= "--{$boundary}\r\nContent-Disposition: form-data; name=\"{$fileField}\"; filename=\"" . basename($path) . "\"\r\n"
        . "Content-Type: {$type}\r\n\r\n" . file_get_contents($path) . "\r\n--{$boundary}--\r\n";
    return [$out, 'multipart/form-data; boundary=' . $boundary];
}

function show(array $result): void
{
    [$status, , $text] = $result;
    $body = json_decode($text, true);
    echo "HTTP {$status}" . PHP_EOL;
    echo json_encode($body ?? ['raw' => $text], JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . PHP_EOL;
    // Some refusals are HTTP 200 with an E return_code (for example E2: image refused): check both.
    $code = is_array($body) ? (string) ($body['return_code'] ?? '') : '';
    if ($status >= 400 || str_starts_with($code, 'E')) {
        exit(1);
    }
}

$command = $argv[1] ?? '';
// Options come after the command as --name=value (getopt() stops at the command word).
$o = [];
foreach (array_slice($argv, 2) as $arg) {
    if (preg_match('/^--([a-z-]+)=(.*)$/', $arg, $m)) {
        $o[$m[1]] = $m[2];
    } else {
        fail("Unrecognised argument: {$arg} (use --name=value)");
    }
}
$need = function (array $names) use ($o): void {
    foreach ($names as $n) {
        if (!isset($o[$n])) {
            fail("--{$n} is required.");
        }
    }
};
$start = new DateTimeImmutable('+5 minutes');
$end = $start->modify('+' . (int) ($o['hours'] ?? 24) . ' hours');

switch ($command) {
    case 'list-offers':
        show(call('GET', '/offers', array_filter(['environment' => 'test', 'limit' => $o['limit'] ?? 20, 'cursor' => $o['cursor'] ?? null])));
        break;

    case 'estimate':
        $need(['lat', 'lng']);
        show(call('POST', '/offers/price-estimate', [], [
            'start_datetime' => iso($start),
            'end_datetime' => iso($end),
            'location' => [(float) $o['lat'], (float) $o['lng']],
            'radius' => (int) ($o['radius'] ?? 10),
            'environment' => 'TEST',
        ]));
        break;

    case 'create-offer':
        $need(['category', 'lat', 'lng']);
        // One Idempotency-Key per offer: a retry with the same key never creates a second offer or payment.
        $idempotencyKey = $o['idempotency-key'] ?? sprintf('%s-%s-4%s-%s-%s', bin2hex(random_bytes(4)), bin2hex(random_bytes(2)), substr(bin2hex(random_bytes(2)), 1), bin2hex(random_bytes(2)), bin2hex(random_bytes(6)));
        fwrite(STDERR, "Idempotency-Key: {$idempotencyKey}" . PHP_EOL);
        [$body, $contentType] = multipart([
            ['environment', 'TEST'],
            ['category_id', (string) $o['category']],
            ['title', '2-for-1 cocktails before 8pm'],
            ['description', 'Show this offer at the bar to get your second cocktail free.'],
            ['terms_and_conditions', 'One per person. Test offer created by the API examples.'],
            ['push_notification_title', '2-for-1 cocktails tonight'],
            ['push_notification_message', 'Show this at the bar before 8pm for a free second cocktail.'],
            ['button_preset', 'book_now'],
            ['url', $o['url'] ?? 'https://www.example.com/offer'],
            ['location[]', (string) $o['lat']],
            ['location[]', (string) $o['lng']],
            ['radius', (string) ($o['radius'] ?? 10)],
            ['start_datetime', iso($start)],
            ['expiry_datetime', iso($end)],
            ['payment_method', $o['payment-method'] ?? 'E'], // E: Stripe test-mode link; B: your Test balance
        ], 'image', $o['image'] ?? SAMPLE_IMAGE);
        show(call('POST', '/offers', [], $body, ['Idempotency-Key' => $idempotencyKey, 'Content-Type' => $contentType]));
        break;

    case 'list-events':
        show(call('GET', '/events', array_filter(['environment' => 'test', 'limit' => $o['limit'] ?? 20, 'cursor' => $o['cursor'] ?? null])));
        break;

    case 'analytics':
        $need(['offer']);
        show(call('GET', '/offers/' . rawurlencode((string) $o['offer']) . '/analytics', ['interval' => $o['interval'] ?? '7d']));
        break;

    default:
        fail('Usage: php agilis-examples.php <list-offers|estimate|create-offer|list-events|analytics> [--option=value]');
}
