// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class PreviewEvent
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.Events.PreviewAsync(new EventPreviewParams
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
            Image = FileUpload.FromPath("/path/to/salsa.jpg"),
        });
        Console.WriteLine(result.BalanceAfter);
    }
}
