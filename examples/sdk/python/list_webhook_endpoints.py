from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.webhook_endpoints.list()
print(len(result["data"]))
