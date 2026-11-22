require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.offers.analytics(45, interval: "30d")
puts result.status
