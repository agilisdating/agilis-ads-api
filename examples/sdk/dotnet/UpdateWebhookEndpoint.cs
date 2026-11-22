// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class UpdateWebhookEndpoint
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.WebhookEndpoints.UpdateAsync("we_01JD2X4Q7N8P9R0S1T2V3W4X5Y", new WebhookEndpointUpdateParams
        {
            EnabledEvents = new[] { "*" },
        });
        Console.WriteLine(result.Status);
    }
}
