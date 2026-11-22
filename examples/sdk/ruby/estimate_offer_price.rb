require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.offers.estimate_price(
  start_datetime: "2027-07-10T08:00:00Z",
  end_datetime: "2027-07-12T20:30:00Z",
  location: [51.5074, -0.1278],
  radius: 10,
  gender: ["Male", "Female"],
  interests: [3, 7]
)
puts result.estimated_cost
