// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.EditEventParams;
import java.nio.file.Path;

public class EditEvent {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.events().edit(
        3104,
        EditEventParams.builder()
            .title("Thursday Comedy Club")
            .url("https://www.barsalsa.co.uk/comedy")
            .image(Path.of("/path/to/salsa.jpg"))
            .build());
    System.out.println(result.getStatus());
  }
}
