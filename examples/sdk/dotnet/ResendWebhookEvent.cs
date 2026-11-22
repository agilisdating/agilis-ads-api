// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class ResendWebhookEvent
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.WebhookEvents.ResendAsync("whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M", new WebhookEventResendParams
        {
            EndpointId = "we_01JD2X4Q7N8P9R0S1T2V3W4X5Y",
        });
        Console.WriteLine(result.WebhookEventId);
    }
}
