from __future__ import annotations

from typing import Any, List

from mcp import StdioServerParameters
from smolagents.mcp_client import MCPClient as _MCPClient


class McpClient:
    """Thin wrapper around ``smolagents`` `MCPClient`.

    It exposes the remote tools as regular Python callables so they can
    cooperate with other agents.
    """

    def __init__(self, params: StdioServerParameters | dict[str, Any] | List[StdioServerParameters | dict[str, Any]]):
        self._client = _MCPClient(params)

    def get_tools(self):
        """Return the list of SmolAgent-compatible tools."""
        return self._client.get_tools()

    def __enter__(self):
        return self._client.__enter__()

    def __exit__(self, exc_type, exc, tb):
        return self._client.__exit__(exc_type, exc, tb)
