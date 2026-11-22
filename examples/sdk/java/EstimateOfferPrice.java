// Generated from https://www.agilis.dating/api-doc. Do not edit.
import dating.agilis.ads.AgilisClient;
import dating.agilis.ads.param.EstimateOfferPriceParams;

public class EstimateOfferPrice {
  public static void main(String[] args) {
    AgilisClient client = AgilisClient.builder().build(); // reads AGILIS_API_KEY

    var result = client.offers().estimatePrice(
        EstimateOfferPriceParams.builder()
            .startDatetime("2027-07-10T08:00:00Z")
            .endDatetime("2027-07-12T20:30:00Z")
            .location(51.5074, -0.1278)
            .radius(10)
            .gender("Male", "Female")
            .interests(3, 7)
            .build());
    System.out.println(result.getEstimatedCost());
  }
}
