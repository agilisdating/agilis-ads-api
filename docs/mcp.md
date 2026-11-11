# Connect an AI assistant with MCP

The Agilis MCP server lets an MCP-capable assistant, such as Claude Code, Cursor or VS Code, read your organisation's advertising data: categories, interests, price estimates, your Offers and Events, and their results. With a Test key it can also create and manage Test Offers and Events.

- **Address:** `https://ads.agilis.dating/api/mcp` (Streamable HTTP).
- **Key:** your Agilis API key, in the `x-api-key` header (or `Authorization: Bearer`).
- **Mode:** the tools work in your key's own mode. A Test key sees Test data, a Live key sees Live data. Start with a Test key.
- **Write tools, Test keys only:** they create and manage Test Offers and Events, which members never see and which are never charged. With a Live key they are refused. No tool takes a payment.

Keep the key in an environment variable, `AGILIS_API_KEY` in the examples below. Never paste it into a chat with your assistant or into a file you commit.

## Claude Code

Add this to `.mcp.json` in your project. Claude Code reads `AGILIS_API_KEY` from your environment:

```json
{
  "mcpServers": {
    "agilis-ads": {
      "type": "http",
      "url": "https://ads.agilis.dating/api/mcp",
      "headers": { "x-api-key": "${AGILIS_API_KEY}" }
    }
  }
}
```

## Cursor

Add this to `~/.cursor/mcp.json`, or `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "agilis-ads": {
      "url": "https://ads.agilis.dating/api/mcp",
      "headers": { "x-api-key": "${env:AGILIS_API_KEY}" }
    }
  }
}
```

## VS Code

Add this to `.vscode/mcp.json`. VS Code asks for the key once and keeps it in its secure storage:

```json
{
  "inputs": [
    { "type": "promptString", "id": "agilis-api-key", "description": "Agilis API key (Test to start)", "password": true }
  ],
  "servers": {
    "agilis-ads": {
      "type": "http",
      "url": "https://ads.agilis.dating/api/mcp",
      "headers": { "x-api-key": "${input:agilis-api-key}" }
    }
  }
}
```

## Other clients

Use the Streamable HTTP transport, the address above, and send your key in the `x-api-key` header from your client's secret store.

## Read tools (any key)

| Tool | What it returns |
|---|---|
| `list_categories` | The Offer categories your organisation may use |
| `list_interests` | Member interests an Offer can be targeted at |
| `estimate_offer_price` | The price of an Offer before it is created; nothing is created or charged |
| `list_offers` | Your Offers, newest first, one page at a time |
| `get_offer_analytics` | One Offer's results over a period |
| `list_event_categories` | The Event categories shown in the app |
| `get_event_config` | Your Event listing fee and your balance |
| `list_events` | Your Events, one page at a time |
| `get_event` | One Event in full |
| `get_event_analytics` | One Event's results over a period |

## Write tools (Test keys only)

| Tool | What it does |
|---|---|
| `create_offer` | Creates a Test Offer, paid from your Test balance |
| `pause_offer` | Pauses one of your Test Offers |
| `resume_offer` | Resumes a paused Test Offer |
| `delete_offer` | Deletes one of your Test Offers |
| `preview_event` | Checks a Test Event before publishing; nothing is published |
| `publish_event` | Publishes a Test Event from your Test balance |
| `edit_event` | Changes details of one of your Test Events |
| `reschedule_event` | Moves a Test Event to new dates |
| `cancel_event` | Cancels one of your Test Events |
| `delete_event` | Deletes one of your Test Events |

Images are given as `image_url`: a public `https` address of a JPEG or PNG. The same image rules apply as for an upload. `create_offer` and `publish_event` accept an optional `idempotency_key`; reuse it to retry safely.

Each call counts towards your key's limit of 60 requests a minute, like a REST request. Full details are in the [API reference](https://www.agilis.dating/api-doc#mcpSection).
