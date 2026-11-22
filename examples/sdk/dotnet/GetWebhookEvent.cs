// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class GetWebhookEvent
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.WebhookEvents.GetAsync("whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M");
        Console.WriteLine(result.Type);
    }
}
