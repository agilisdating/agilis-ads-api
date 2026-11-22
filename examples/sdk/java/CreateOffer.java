// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.CreateOfferParams;
import java.nio.file.Path;

public class CreateOffer {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    // An Idempotency-Key is sent for you, and reused if the request is retried.
    var result = client.offers().create(
        CreateOfferParams.builder()
            .categoryId(1)
            .title("20% off summer sale")
            .description("Discount valid through July")
            .termsAndConditions("Valid online only.")
            .pushNotificationTitle("20% off this summer")
            .pushNotificationMessage("Show this at the till for 20% off everything until the end of July.")
            .buttonPreset("book_now")
            .url("https://advertiseroffer.com")
            .location(51.5074, -0.1278)
            .radius(10)
            .gender("Male", "Female")
            .interests(3, 7)
            .startDatetime("2027-07-10T08:00:00Z")
            .expiryDatetime("2027-07-12T20:30:00Z")
            .paymentMethod("E")
            .image(Path.of("/path/to/offer.jpg"))
            .build());
    System.out.println(result.getOfferId());
  }
}
