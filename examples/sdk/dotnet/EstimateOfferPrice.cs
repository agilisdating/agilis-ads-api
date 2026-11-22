// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class EstimateOfferPrice
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.Offers.EstimatePriceAsync(new OfferPriceEstimateParams
        {
            StartDatetime = DateTimeOffset.Parse("2027-07-10T08:00:00Z"),
            EndDatetime = DateTimeOffset.Parse("2027-07-12T20:30:00Z"),
            Location = new GeoLocation(51.5074, -0.1278),
            Radius = 10,
            Gender = new[] { "Male", "Female" },
            Interests = new[] { 3, 7 },
        });
        Console.WriteLine(result.EstimatedCost);
    }
}
