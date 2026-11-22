// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;

public class GetWebhookEvent {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.webhookEvents().get("whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M");
    System.out.println(result.getType());
  }
}
