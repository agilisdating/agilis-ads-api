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

	result, err := client.WebhookEvents.Get(ctx, "whevt_01JD2Y8B3C4D5E6F7G8H9J0K1M")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.Type)
}
