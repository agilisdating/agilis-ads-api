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

	result, err := client.Events.Delete(ctx, 3104, nil)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.Message)
}
