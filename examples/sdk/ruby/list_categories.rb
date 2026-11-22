require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.categories.list
puts result.categories.length
