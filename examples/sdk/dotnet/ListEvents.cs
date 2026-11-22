// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class ListEvents
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.Events.ListAsync(new EventListParams
        {
            Limit = 20,
        });
        Console.WriteLine(result.Data.Count);
    }
}
