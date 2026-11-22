// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class PublishEvent
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        // An Idempotency-Key is sent for you, and reused if the request is retried.
        var result = await client.Events.PublishAsync(new EventPublishParams
        {
            Title = "Beginners Cuban Salsa: Friday Social",
            Description = "Drop-in class for absolute beginners, followed by a social until late. No partner needed.",
            VenueName = "Bar Salsa",
            Address = "96 Charing Cross Road",
            City = "London",
            CountryCode = "GB",
            Location = new GeoLocation(51.5133, -0.1300),
            StartsAt = DateTimeOffset.Parse("2027-10-16T18:30:00Z"),
            EndsAt = DateTimeOffset.Parse("2027-10-16T23:00:00Z"),
            Url = "https://www.barsalsa.co.uk/classes/friday",
            PriceMin = 12m,
            PriceMax = 12m,
            Currency = "GBP",
            PaymentMethod = "B",
            PreviewToken = "evp_8f3c1a…",
        });
        Console.WriteLine(result.EventId);
    }
}
