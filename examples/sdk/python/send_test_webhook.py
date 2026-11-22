from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.webhook_endpoints.send_test("we_01JD2X4Q7N8P9R0S1T2V3W4X5Y", {
    "type": "offer.started",
})
print(result["webhook_event_id"])
