from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.webhook_endpoints.create({
    "url": "https://hooks.example.com/agilis",
    "enabled_events": ["offer.started", "offer.ended", "event.published"],
    "description": "Order system",
})
print(result["secret"])
