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

	result, err := client.Offers.EstimatePrice(ctx, &agilisads.EstimateOfferPriceParams{
		StartDatetime: "2027-07-10T08:00:00Z",
		EndDatetime:   "2027-07-12T20:30:00Z",
		Location:      agilisads.LatLng{Latitude: 51.5074, Longitude: -0.1278},
		Radius:        10,
		Gender:        []string{"Male", "Female"},
		Interests:     []int64{3, 7},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.EstimatedCost)
}
