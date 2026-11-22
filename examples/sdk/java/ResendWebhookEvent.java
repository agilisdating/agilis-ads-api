// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.ResendWebhookEventParams;

public class ResendWebhookEvent {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.webhookEvents().resend(
        "whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M",
        ResendWebhookEventParams.builder()
            .endpointId("we_01JD2X4Q7N8P9R0S1T2V3W4X5Y")
            .build());
    System.out.println(result.getWebhookEventId());
  }
}
