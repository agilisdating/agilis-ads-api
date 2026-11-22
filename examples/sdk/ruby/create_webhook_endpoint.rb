require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.webhook_endpoints.create(
  url: "https://hooks.example.com/agilis",
  enabled_events: ["offer.started", "offer.ended", "event.published"],
  description: "Order system"
)
puts result.secret
