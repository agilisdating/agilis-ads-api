// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.PreviewEventParams;
import java.nio.file.Path;
import java.util.List;

public class PreviewEvent {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.events().preview(
        PreviewEventParams.builder()
            .title("Beginners Cuban Salsa: Friday Social")
            .description("Drop-in class for absolute beginners, followed by a social until late. No partner needed.")
            .venueName("Bar Salsa")
            .put("address", "96 Charing Cross Road")
            .put("city", "London")
            .put("country_code", "GB")
            .put("location", List.of(51.5133, -0.1300))
            .put("starts_at", "2027-10-16T18:30:00Z")
            .put("ends_at", "2027-10-16T23:00:00Z")
            .put("url", "https://www.barsalsa.co.uk/classes/friday")
            .put("price_min", 12)
            .put("price_max", 12)
            .put("currency", "GBP")
            .image(Path.of("/path/to/salsa.jpg"))
            .build());
    System.out.println(result.getBalanceAfter());
  }
}
