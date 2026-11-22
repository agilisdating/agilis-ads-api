require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.offers.resume(45)
puts result.message
