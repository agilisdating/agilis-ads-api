require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.webhook_events.get("whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M")
puts result.type
