from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.events.cancel(3104)
print(result["status"])
