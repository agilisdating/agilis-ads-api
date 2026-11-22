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

	result, err := client.Offers.Analytics(ctx, 45, &agilisads.AnalyticsParams{Interval: "30d"})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.Status)
}
