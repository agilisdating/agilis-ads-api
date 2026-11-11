# Connect an AI assistant with MCP

The Agilis MCP server lets an MCP-capable assistant, such as Claude Code, Cursor or VS Code, read your organisation's advertising data: categories, interests, price estimates, your Offers and Events, and their results.

- **Address:** `https://ads.agilis.dating/api/mcp` (Streamable HTTP).
- **Key:** your Agilis API key, in the `x-api-key` header (or `Authorization: Bearer`).
- **Mode:** the tools work in your key's own mode. A Test key sees Test data, a Live key sees Live data. Start with a Test key.
- **Read-only:** the tools never create, change, pay for or delete anything.

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

## Tools

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

Each call counts towards your key's limit of 60 requests a minute, like a REST request. Full details are in the [API reference](https://www.agilis.dating/api-doc#mcpSection).
