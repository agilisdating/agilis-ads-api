from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.event_currencies.list()
print(len(result["currencies"]))
