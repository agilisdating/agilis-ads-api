// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class RescheduleEvent
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.Events.RescheduleAsync(3104, new EventRescheduleParams
        {
            StartsAt = DateTimeOffset.Parse("2027-10-23T18:30:00Z"),
            EndsAt = DateTimeOffset.Parse("2027-10-23T23:00:00Z"),
        });
        Console.WriteLine(result.Status);
    }
}
