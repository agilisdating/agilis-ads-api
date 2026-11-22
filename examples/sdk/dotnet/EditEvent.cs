// Generated from https://www.agilis.dating/api-doc. Do not edit.
using Agilis.Ads;

namespace AgilisExamples;

public static class EditEvent
{
    public static async Task RunAsync()
    {
        using var client = new AgilisClient(); // reads AGILIS_API_KEY

        var result = await client.Events.EditAsync(3104, new EventEditParams
        {
            Title = "Thursday Comedy Club",
            Url = "https://www.barsalsa.co.uk/comedy",
            Image = FileUpload.FromPath("/path/to/salsa.jpg"),
        });
        Console.WriteLine(result.Status);
    }
}
