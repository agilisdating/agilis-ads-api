require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.interests.list
puts result.interests.length
