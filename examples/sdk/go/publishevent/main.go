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
	result, err := client.Events.Publish(ctx, &agilisads.PublishEventParams{
		Title:         "Beginners Cuban Salsa: Friday Social",
		Description:   "Drop-in class for absolute beginners, followed by a social until late. No partner needed.",
		VenueName:     "Bar Salsa",
		Address:       "96 Charing Cross Road",
		City:          "London",
		CountryCode:   "GB",
		Location:      agilisads.LatLng{Latitude: 51.5133, Longitude: -0.1300},
		StartsAt:      "2027-10-16T18:30:00Z",
		EndsAt:        "2027-10-16T23:00:00Z",
		URL:           "https://www.barsalsa.co.uk/classes/friday",
		PriceMin:      agilisads.Float64(12),
		PriceMax:      agilisads.Float64(12),
		Currency:      "GBP",
		PaymentMethod: "B",
		PreviewToken:  "evp_8f3c1a…",
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.EventID)
}
