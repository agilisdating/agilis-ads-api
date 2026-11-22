// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.ListEventsParams;

public class ListEvents {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.events().list(
        ListEventsParams.builder()
            .limit(20)
            .build());
    System.out.println(result.getData().size());
  }
}
