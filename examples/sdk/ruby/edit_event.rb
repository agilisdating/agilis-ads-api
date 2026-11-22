require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.events.edit(
  3104,
  title: "Thursday Comedy Club",
  url: "https://www.barsalsa.co.uk/comedy",
  image: "/path/to/salsa.jpg"
)
puts result.status
