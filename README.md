# Wikipedia MCP Server

A Model Context Protocol server that provides capabilities to query Wikipedia. This server enables LLMs to get information from Wikipedia.

## Available Tools

- `search` - Search `keyword` on Wikipedia.
  - Required arguments:
    - `keyword` (string): The search keyword
    - `language` (string): The language

- `fetch` - Fetch Wikipedia page content.
  - Required arguments:
    - `id` (integer): The pade ID
    - `language` (string): The language

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run *wikipedia-mcp*.

### Using PIP

Alternatively you can install `wikipedia-mcp` via pip:

```bash
pip install wikipedia-mcp-server
```

After installation, you can run it as a script using:

```bash
python -m wikipedia_mcp
```

## Configurations

### Using uvx
```json
{
  "mcpServers": {
    "wikipedia-mcp": {
      "command": "uvx",
      "args": [
        "wikipedia-mcp-server@latest"
      ]
    }
  }
}
```

### Using docker
```json
{
  "mcpServers": {
    "wikipedia-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "ghcr.io/progamesigner/wikipedia-mcp:latest"
      ]
    }
  }
}
```

### Using pip installation
```json
{
  "mcpServers": {
    "wikipedia-mcp": {
      "command": "python",
      "args": [
        "-m",
        "wikipedia_mcp"
      ]
    }
  }
}
```

## Build

Docker build:

```bash
docker build -t wikipedia-mcp .
```
