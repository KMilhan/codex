# Yowon

`yowon` is a tiny Python project built with [uv](https://github.com/astral-sh/uv). It exposes a CLI and an MCP server that rely exclusively on the OpenAI model via `smolagents`.

## Usage

### CLI

```bash
yowon run "Hello"
```

For a conversation that keeps context between prompts:

```bash
yowon chat
```

### MCP Server

```bash
yowon serve
```

This will start an MCP server over stdio so it can cooperate with other agents.
