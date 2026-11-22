require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.events.analytics(3104, interval: "30d")
puts result.status
