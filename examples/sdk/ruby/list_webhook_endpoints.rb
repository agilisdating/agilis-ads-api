require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.webhook_endpoints.list
puts result.data.length
