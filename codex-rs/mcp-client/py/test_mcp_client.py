import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
from mcp import StdioServerParameters
from mcp_client import McpClient

SERVER_SCRIPT = r"""
import anyio
from mcp.server.lowlevel.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, Tool, TextContent

server = Server("py-test")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="ping",
            description="ping",
            inputSchema={
                "type": "object",
                "properties": {"text": {"type": "string", "description": "ignored"}},
            },
        )
    ]

@server.call_tool()
async def call_tool(name, arguments):
    return [TextContent(text="pong")]

async def main():
    async with stdio_server() as (r, w):
        await server.run(r, w, InitializationOptions(server_name="py-test", server_version="0.1", capabilities=ServerCapabilities()))

anyio.run(main)
"""


class McpClientTests(unittest.TestCase):
    def test_can_list_tools(self):
        params = StdioServerParameters(command=sys.executable, args=["-u", "-c", SERVER_SCRIPT])
        client = McpClient(params)
        with client as tools:
            self.assertEqual(len(tools), 1)
            self.assertEqual(tools[0].name, "ping")

if __name__ == "__main__":
    unittest.main()
