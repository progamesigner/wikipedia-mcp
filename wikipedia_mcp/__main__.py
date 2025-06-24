from asyncio import run

from wikipedia_mcp.server import mcp

if __name__ == '__main__':
    run(mcp.run_async())
