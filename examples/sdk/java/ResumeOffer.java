// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;

public class ResumeOffer {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.offers().resume(45);
    System.out.println(result.getMessage());
  }
}
