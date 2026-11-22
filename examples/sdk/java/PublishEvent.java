// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.PublishEventParams;

public class PublishEvent {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    // An Idempotency-Key is sent for you, and reused if the request is retried.
    var result = client.events().publish(
        PublishEventParams.builder()
            .title("Beginners Cuban Salsa: Friday Social")
            .description("Drop-in class for absolute beginners, followed by a social until late. No partner needed.")
            .venueName("Bar Salsa")
            .address("96 Charing Cross Road")
            .city("London")
            .countryCode("GB")
            .location(51.5133, -0.1300)
            .startsAt("2027-10-16T18:30:00Z")
            .endsAt("2027-10-16T23:00:00Z")
            .url("https://www.barsalsa.co.uk/classes/friday")
            .priceMin(12)
            .priceMax(12)
            .currency("GBP")
            .paymentMethod("B")
            .previewToken("evp_8f3c1a…")
            .build());
    System.out.println(result.getEventId());
  }
}
