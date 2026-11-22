// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;

public class ListEventCategories {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.eventCategories().list();
    System.out.println(result.getCategories().size());
  }
}
