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

	result, err := client.WebhookEvents.Resend(ctx, "whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M", &agilisads.ResendWebhookEventParams{
		EndpointID: "we_01JD2X4Q7N8P9R0S1T2V3W4X5Y",
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.WebhookEventID)
}
