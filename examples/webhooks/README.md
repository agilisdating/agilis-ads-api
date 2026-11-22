# Checking a webhook signature

Every message Agilis sends to your webhook endpoint carries an `Agilis-Signature` header:

```
Agilis-Signature: t=1795075200,v1=5257a869e7ecebeda32affa62cdca3fa51cad7e77a0e56ff536d0ce8e108d8bd
```

To check it:

1. Read the request body **exactly as received**, before any JSON parsing.
2. Split the header on commas: `t` is the timestamp, each `v1` a signature. While a rolled secret is still valid there is one `v1` per secret.
3. Compute the hex HMAC-SHA256 of `<t>.<raw body>` with your endpoint secret (`whsec_…`).
4. Accept the message if any `v1` equals it, compared in constant time, and `t` is within 5 minutes of now.

Then answer with any 2xx status within 10 seconds, and ignore an `id` you have already handled.

| Language | File | Run |
|---|---|---|
| Node.js | [verify.js](verify.js) | `node verify.js body.json` |
| Python | [verify.py](verify.py) | `python verify.py body.json` |
| PHP | [verify.php](verify.php) | `php verify.php body.json` |
| C# (.NET) | [dotnet/Program.cs](dotnet/Program.cs) | `dotnet run --project dotnet -- body.json` |
| Java 17+ | [Verify.java](Verify.java) | `java Verify.java body.json` |
| Go | [verify.go](verify.go) | `go run verify.go body.json` |
| Ruby | [verify.rb](verify.rb) | `ruby verify.rb body.json` |

Each reads the header from `AGILIS_SIGNATURE` and the secret from `AGILIS_WEBHOOK_SECRET`, prints `verified` and the event type, or exits with status 1. In your own server, call the function with the request's raw body and header.

[sample-event.json](sample-event.json) is an example `offer.ended` message. Every event type, with an example, is in the [API reference](https://www.agilis.dating/api-doc#webhookEventTypes).
