from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.offers.pause(45)
print(result["message"])
