require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.webhook_endpoints.roll_secret(
  "we_01JD2X4Q7N8P9R0S1T2V3W4X5Y",
  expires_in: "24h"
)
puts result.secret
