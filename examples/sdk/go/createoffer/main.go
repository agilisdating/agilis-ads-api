package main

import (
	"context"
	"fmt"
	"log"

	agilisads "github.com/agilisdating/agilis-ads-go"
)

func main() {
	client := agilisads.NewClient("") // reads AGILIS_API_KEY
	ctx := context.Background()

	// An Idempotency-Key is sent for you, and reused if the request is retried.
	result, err := client.Offers.Create(ctx, &agilisads.CreateOfferParams{
		CategoryID:              1,
		Title:                   "20% off summer sale",
		Description:             "Discount valid through July",
		TermsAndConditions:      agilisads.String("Valid online only."),
		PushNotificationTitle:   "20% off this summer",
		PushNotificationMessage: "Show this at the till for 20% off everything until the end of July.",
		ButtonPreset:            "book_now",
		URL:                     "https://advertiseroffer.com",
		Location:                agilisads.LatLng{Latitude: 51.5074, Longitude: -0.1278},
		Radius:                  10,
		Gender:                  []string{"Male", "Female"},
		Interests:               []int64{3, 7},
		StartDatetime:           "2027-07-10T08:00:00Z",
		ExpiryDatetime:          "2027-07-12T20:30:00Z",
		PaymentMethod:           "E",
		Image:                   agilisads.FileFromPath("/path/to/offer.jpg"),
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.OfferID)
}
