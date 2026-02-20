# MCP Remote Setup Guide

How to connect to Anny's MCP server over HTTPS using the Streamable HTTP transport. This lets Claude Desktop and Claude Code access your analytics tools remotely — no local install needed.

For local stdio setup, see [MCP Stdio Setup](MCP-STDIO-SETUP.md).

## Prerequisites

- Anny deployed and running (e.g. at `https://anny.membies.com`)
- Your `ANNY_API_KEY` value (the same key used for REST API auth)

## Claude Desktop

Add Anny to your Claude Desktop config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "anny": {
      "type": "streamable-http",
      "url": "https://anny.membies.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY_HERE"
      }
    }
  }
}
```

Replace `YOUR_API_KEY_HERE` with your actual `ANNY_API_KEY` value.

Restart Claude Desktop after saving the config.

## Claude Code

Add Anny as a remote MCP server:

```bash
claude mcp add anny --transport http https://anny.membies.com/mcp \
  --header "Authorization: Bearer YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with your actual `ANNY_API_KEY` value.

## Verifying the Connection

Once configured, you should see 21 Anny tools available. Test with the `ping` tool — it should return `pong`.

## Authentication

The MCP endpoint uses Bearer token authentication:

- **Header:** `Authorization: Bearer <ANNY_API_KEY>`
- Same key as REST API (`X-API-Key` header)
- When `ANNY_API_KEY` is empty on the server, auth is disabled (dev mode)

## Troubleshooting

**401 Unauthorized:**
- Verify your API key matches the `ANNY_API_KEY` set on the server
- Check the `Authorization: Bearer` header format (note the space after "Bearer")

**Connection refused:**
- Confirm the server is running: `curl https://anny.membies.com/health`
- Check that `/mcp` is accessible through the reverse proxy

**No tools appear:**
- Restart the MCP client after saving the config
- Check the client's MCP logs for connection or auth errors
