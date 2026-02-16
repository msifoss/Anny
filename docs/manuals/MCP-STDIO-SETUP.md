# MCP Stdio Setup Guide

How to connect Anny as an MCP server to Claude Desktop, Claude Code, or any MCP-compatible client using the stdio transport.

## Prerequisites

- Anny installed locally (`make install`) or via Docker
- Service account credentials configured (see [Service Account Setup](SERVICE-ACCOUNT-SETUP.md))
- A `.env` file in the project root with your Google credentials

## Claude Desktop

Add Anny to your Claude Desktop config file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

### Option A: Local install

```json
{
  "mcpServers": {
    "anny": {
      "command": "/path/to/Anny/.venv/bin/python",
      "args": ["-m", "anny.cli.mcp_stdio"],
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_KEY_PATH": "/path/to/service-account-key.json",
        "GA4_PROPERTY_ID": "properties/123456789",
        "SEARCH_CONSOLE_SITE_URL": "https://example.com"
      }
    }
  }
}
```

Replace the paths and property values with your own.

### Option B: Docker

```json
{
  "mcpServers": {
    "anny": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-v", "/path/to/service-account-key.json:/secrets/service-account.json:ro",
        "-e", "GOOGLE_SERVICE_ACCOUNT_KEY_PATH=/secrets/service-account.json",
        "-e", "GA4_PROPERTY_ID=properties/123456789",
        "-e", "SEARCH_CONSOLE_SITE_URL=https://example.com",
        "anny",
        "python", "-m", "anny.cli.mcp_stdio"
      ]
    }
  }
}
```

Build the image first with `make docker-build`.

## Claude Code

Add Anny to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "anny": {
      "command": ".venv/bin/python",
      "args": ["-m", "anny.cli.mcp_stdio"],
      "env": {
        "GOOGLE_SERVICE_ACCOUNT_KEY_PATH": "/path/to/service-account-key.json",
        "GA4_PROPERTY_ID": "properties/123456789",
        "SEARCH_CONSOLE_SITE_URL": "https://example.com"
      }
    }
  }
}
```

## Verifying the Connection

Once configured, restart your MCP client. You should see 12 Anny tools available:

| Tool | Description |
|------|-------------|
| `ping` | Health check |
| `ga4_report` | Custom GA4 report |
| `ga4_top_pages` | Top pages by page views |
| `ga4_traffic_summary` | Traffic by source |
| `search_console_query` | Custom search analytics query |
| `search_console_top_queries` | Top search queries |
| `search_console_top_pages` | Top pages by clicks |
| `search_console_summary` | Overall search performance |
| `gtm_list_accounts` | List GTM accounts |
| `gtm_list_containers` | List containers for an account |
| `gtm_container_setup` | Container tags/triggers/variables summary |
| `gtm_list_tags` | List tags in a container |

Test with the `ping` tool — it should return `pong`.

## Troubleshooting

**"Command not found" or server won't start:**
- Verify the Python path is correct (`which python` inside your venv)
- Ensure Anny is installed: `.venv/bin/pip show anny`

**"AuthError" or credential failures:**
- Check that `GOOGLE_SERVICE_ACCOUNT_KEY_PATH` points to a valid JSON key file
- Verify the service account has been granted access to your GA4 property, Search Console site, or GTM account

**No tools appear:**
- Restart the MCP client after saving the config
- Check the client's MCP logs for connection errors
