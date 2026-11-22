using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

// Verifies an Agilis webhook signature. Usage: AGILIS_WEBHOOK_SECRET=whsec_... AGILIS_SIGNATURE='t=...,v1=...' dotnet run --project dotnet -- body.json
try
{
    using var doc = VerifyAgilisWebhook(File.ReadAllText(args[0]), Environment.GetEnvironmentVariable("AGILIS_SIGNATURE") ?? "",
        Environment.GetEnvironmentVariable("AGILIS_WEBHOOK_SECRET") ?? "");
    Console.WriteLine("verified " + doc.RootElement.GetProperty("type").GetString());
}
catch (InvalidOperationException e)
{
    Console.Error.WriteLine("rejected: " + e.Message);
    Environment.Exit(1);
}

// rawBody: the request body exactly as received, read as a string before any JSON parsing.
static JsonDocument VerifyAgilisWebhook(string rawBody, string header, string secret, int toleranceSeconds = 300)
{
    string? t = null;
    var signatures = new List<string>();
    foreach (var part in (header ?? "").Split(','))
    {
        var kv = part.Trim().Split('=', 2);
        if (kv.Length != 2) continue;
        if (kv[0] == "t") t = kv[1];
        if (kv[0] == "v1") signatures.Add(kv[1]);
    }
    if (t is null || !long.TryParse(t, out var ts) || signatures.Count == 0)
        throw new InvalidOperationException("Invalid signature header");
    using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(secret));
    var expected = Convert.ToHexString(hmac.ComputeHash(Encoding.UTF8.GetBytes($"{t}.{rawBody}"))).ToLowerInvariant();
    var ok = signatures.Any(s => CryptographicOperations.FixedTimeEquals(Encoding.UTF8.GetBytes(s), Encoding.UTF8.GetBytes(expected)));
    if (!ok) throw new InvalidOperationException("Signature does not match");
    if (Math.Abs(DateTimeOffset.UtcNow.ToUnixTimeSeconds() - ts) > toleranceSeconds)
        throw new InvalidOperationException("Timestamp outside the tolerance");
    return JsonDocument.Parse(rawBody);
}
