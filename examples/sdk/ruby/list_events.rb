require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.events.list(
  limit: 20
)
puts result.data.length
