require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.webhook_endpoints.update(
  "we_01JD2X4Q7N8P9R0S1T2V3W4X5Y",
  enabled_events: ["*"]
)
puts result.status
