from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.events.analytics(3104, {"interval": "30d"})
print(result["status"])
