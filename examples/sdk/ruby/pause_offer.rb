require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.offers.pause(45)
puts result.message
