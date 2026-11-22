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

	result, err := client.WebhookEndpoints.Update(ctx, "we_01JD2X4Q7N8P9R0S1T2V3W4X5Y", &agilisads.UpdateWebhookEndpointParams{
		EnabledEvents: []string{"*"},
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.Status)
}
