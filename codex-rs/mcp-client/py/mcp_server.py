"""Minimal MCP server implemented in Python using the `mcp` package."""

import anyio
from mcp.server.lowlevel.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import ServerCapabilities, Tool, TextContent

server = Server("codex-python")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="echo",
            description="Echo input text",
            inputSchema={"type": "object", "properties": {"text": {"type": "string", "description": "text to echo"}}},
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict | None):
    if name == "echo":
        text = (arguments or {}).get("text", "")
        return [TextContent(text=text)]
    raise ValueError(f"unknown tool: {name}")

async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(
            read,
            write,
            InitializationOptions(
                server_name="codex-python",
                server_version="0.1",
                capabilities=ServerCapabilities(),
            ),
        )

if __name__ == "__main__":
    anyio.run(main)
