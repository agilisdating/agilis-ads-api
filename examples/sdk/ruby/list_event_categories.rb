require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.event_categories.list
puts result.categories.length
