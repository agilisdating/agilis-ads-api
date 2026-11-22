from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.offers.list({
    "limit": 20,
})
print(len(result["data"]))
