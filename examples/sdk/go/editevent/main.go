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

	result, err := client.Events.Edit(ctx, 3104, &agilisads.EditEventParams{
		Title: agilisads.String("Thursday Comedy Club"),
		URL:   agilisads.String("https://www.barsalsa.co.uk/comedy"),
		Image: agilisads.FileFromPath("/path/to/salsa.jpg"),
	})
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(result.Status)
}
