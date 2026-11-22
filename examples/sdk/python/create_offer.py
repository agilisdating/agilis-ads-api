from agilis_ads import Agilis

client = Agilis()  # reads AGILIS_API_KEY

# An Idempotency-Key is sent for you, and reused if the request is retried.
result = client.offers.create({
    "category_id": 1,
    "title": "20% off summer sale",
    "description": "Discount valid through July",
    "terms_and_conditions": "Valid online only.",
    "push_notification_title": "20% off this summer",
    "push_notification_message": "Show this at the till for 20% off everything until the end of July.",
    "button_preset": "book_now",
    "url": "https://advertiseroffer.com",
    "location": [51.5074, -0.1278],
    "radius": 10,
    "gender": ["Male", "Female"],
    "interests": [3, 7],
    "start_datetime": "2027-07-10T08:00:00Z",
    "expiry_datetime": "2027-07-12T20:30:00Z",
    "payment_method": "E",
    "image": "/path/to/offer.jpg",
})
print(result["offer_id"])
