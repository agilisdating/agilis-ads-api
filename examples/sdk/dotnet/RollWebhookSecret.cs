// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class RollWebhookSecret
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.WebhookEndpoints.RollSecretAsync("we_01JD2X4Q7N8P9R0S1T2V3W4X5Y", new WebhookSecretRollParams
        {
            ExpiresIn = "24h",
        });
        Console.WriteLine(result.Secret);
    }
}
