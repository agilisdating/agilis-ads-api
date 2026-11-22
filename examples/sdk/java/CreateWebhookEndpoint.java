// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.CreateWebhookEndpointParams;

public class CreateWebhookEndpoint {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.webhookEndpoints().create(
        CreateWebhookEndpointParams.builder()
            .url("https://hooks.example.com/agilis")
            .enabledEvents("offer.started", "offer.ended", "event.published")
            .description("Order system")
            .build());
    System.out.println(result.getSecret());
  }
}
