// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.RescheduleEventParams;

public class RescheduleEvent {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.events().reschedule(
        3104,
        RescheduleEventParams.builder()
            .startsAt("2027-10-23T18:30:00Z")
            .endsAt("2027-10-23T23:00:00Z")
            .build());
    System.out.println(result.getStatus());
  }
}
