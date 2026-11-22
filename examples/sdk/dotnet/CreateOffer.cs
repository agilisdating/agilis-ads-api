// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class CreateOffer
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        // An Idempotency-Key is sent for you, and reused if the request is retried.
        var result = await client.Offers.CreateAsync(new OfferCreateParams
        {
            CategoryId = 1,
            Title = "20% off summer sale",
            Description = "Discount valid through July",
            TermsAndConditions = "Valid online only.",
            PushNotificationTitle = "20% off this summer",
            PushNotificationMessage = "Show this at the till for 20% off everything until the end of July.",
            ButtonPreset = "book_now",
            Url = "https://advertiseroffer.com",
            Location = new GeoLocation(51.5074, -0.1278),
            Radius = 10,
            Gender = new[] { "Male", "Female" },
            Interests = new[] { 3, 7 },
            StartDatetime = DateTimeOffset.Parse("2027-07-10T08:00:00Z"),
            ExpiryDatetime = DateTimeOffset.Parse("2027-07-12T20:30:00Z"),
            PaymentMethod = "E",
            Image = FileUpload.FromPath("/path/to/offer.jpg"),
        });
        Console.WriteLine(result.OfferId);
    }
}
