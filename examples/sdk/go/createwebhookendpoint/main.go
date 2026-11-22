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

	result, err := client.WebhookEndpoints.Create(ctx, &agilisads.CreateWebhookEndpointParams{
		URL:           "https://hooks.example.com/agilis",
		EnabledEvents: []string{"offer.started", "offer.ended", "event.published"},
		Description:   agilisads.String("Order system"),
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.Secret)
}
