from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.webhook_events.resend("whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M", {
    "endpoint_id": "we_01JD2X4Q7N8P9R0S1T2V3W4X5Y",
})
print(result["webhook_event_id"])
