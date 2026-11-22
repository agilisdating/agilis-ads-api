// Verifies an Agilis webhook signature. Usage: AGILIS_WEBHOOK_SECRET=whsec_... AGILIS_SIGNATURE='t=...,v1=...' go run verify.go body.json
package main

import (
	"fmt"
	"os"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"math"
	"strconv"
	"strings"
	"time"
)

// rawBody: the request body exactly as received (io.ReadAll(r.Body)), before any JSON parsing.
// Pass tolerance 5 * time.Minute.
func VerifyAgilisWebhook(rawBody []byte, header, secret string, tolerance time.Duration) (map[string]any, error) {
	var t string
	var signatures []string
	for _, part := range strings.Split(header, ",") {
		k, v, found := strings.Cut(strings.TrimSpace(part), "=")
		if !found {
			continue
		}
		switch k {
		case "t":
			t = v
		case "v1":
			signatures = append(signatures, v)
		}
	}
	ts, err := strconv.ParseInt(t, 10, 64)
	if err != nil || len(signatures) == 0 {
		return nil, errors.New("invalid signature header")
	}
	mac := hmac.New(sha256.New, []byte(secret))
	mac.Write([]byte(t + "."))
	mac.Write(rawBody)
	expected := hex.EncodeToString(mac.Sum(nil))
	ok := false
	for _, s := range signatures {
		ok = ok || hmac.Equal([]byte(expected), []byte(s))
	}
	if !ok {
		return nil, errors.New("signature does not match")
	}
	if math.Abs(float64(time.Now().Unix()-ts)) > tolerance.Seconds() {
		return nil, errors.New("timestamp outside the tolerance")
	}
	var event map[string]any
	return event, json.Unmarshal(rawBody, &event)
}

func main() {
	body, err := os.ReadFile(os.Args[1])
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	event, err := VerifyAgilisWebhook(body, os.Getenv("AGILIS_SIGNATURE"), os.Getenv("AGILIS_WEBHOOK_SECRET"), 5*time.Minute)
	if err != nil {
		fmt.Fprintln(os.Stderr, "rejected:", err)
		os.Exit(1)
	}
	fmt.Println("verified", event["type"])
}
