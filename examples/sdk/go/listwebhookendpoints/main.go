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

	result, err := client.WebhookEndpoints.List(ctx)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(len(result.Data))
}
