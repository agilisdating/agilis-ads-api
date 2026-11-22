// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;

public class DeleteWebhookEndpoint {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.webhookEndpoints().delete("we_01JD2X4Q7N8P9R0S1T2V3W4X5Y");
    System.out.println(result.getDeleted());
  }
}
