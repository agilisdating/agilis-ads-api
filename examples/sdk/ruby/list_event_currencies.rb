require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.event_currencies.list
puts result.currencies.length
