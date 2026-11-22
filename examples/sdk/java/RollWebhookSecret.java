// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.RollWebhookSecretParams;

public class RollWebhookSecret {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.webhookEndpoints().rollSecret(
        "we_01JD2X4Q7N8P9R0S1T2V3W4X5Y",
        RollWebhookSecretParams.builder()
            .expiresIn("24h")
            .build());
    System.out.println(result.getSecret());
  }
}
