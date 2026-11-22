require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.events.delete(3104)
puts result.message
