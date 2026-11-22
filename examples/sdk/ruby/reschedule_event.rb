require "agilis_ads"

client = AgilisAds::Client.new # reads AGILIS_API_KEY

result = client.events.reschedule(
  3104,
  starts_at: "2027-10-23T18:30:00Z",
  ends_at: "2027-10-23T23:00:00Z"
)
puts result.status
