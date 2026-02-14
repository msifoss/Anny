"""Standalone stdio entry point for the Anny MCP server.

Run with: python -m anny.cli.mcp_stdio
"""

from anny.mcp_server import mcp

if __name__ == "__main__":
    mcp.run()
