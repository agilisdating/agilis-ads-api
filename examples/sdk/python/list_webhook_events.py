from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.webhook_events.list({
    "delivery_success": False,
    "limit": 20,
})
print(len(result["data"]))
