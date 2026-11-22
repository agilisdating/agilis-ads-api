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

	result, err := client.Events.Reschedule(ctx, 3104, &agilisads.RescheduleEventParams{
		StartsAt: "2027-10-23T18:30:00Z",
		EndsAt:   "2027-10-23T23:00:00Z",
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.Status)
}
