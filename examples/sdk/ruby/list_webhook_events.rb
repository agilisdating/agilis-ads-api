require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.webhook_events.list(
  delivery_success: false,
  limit: 20
)
puts result.data.length
