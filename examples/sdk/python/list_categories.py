from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

result = client.categories.list()
print(len(result["categories"]))
