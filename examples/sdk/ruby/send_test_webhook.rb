require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.webhook_endpoints.send_test(
  "we_01JD2X4Q7N8P9R0S1T2V3W4X5Y",
  type: "offer.started"
)
puts result.webhook_event_id
