// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class CreateWebhookEndpoint
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.WebhookEndpoints.CreateAsync(new WebhookEndpointCreateParams
        {
            Url = "https://hooks.example.com/agilis",
            EnabledEvents = new[] { "offer.started", "offer.ended", "event.published" },
            Description = "Order system",
        });
        Console.WriteLine(result.Secret);
    }
}
