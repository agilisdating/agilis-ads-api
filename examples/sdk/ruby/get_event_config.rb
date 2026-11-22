require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.event_config.get
puts result.currency
