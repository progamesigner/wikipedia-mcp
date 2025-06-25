from typing import Annotated

from fastmcp.server.server import Transport
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: Annotated[str | None, Field(alias='SERVE_HOST')] = None
    path: Annotated[str | None, Field(alias='SERVE_PATH')] = None
    port: Annotated[int | None, Field(alias='SERVE_PORT')] = None
    transport: Annotated[Transport, Field()] = 'stdio'


def main() -> int:
    from asyncio import run

    from wikipedia_mcp.server import mcp

    settings = Settings()

    if settings.transport in {'stdio'}:
        run(mcp.run_async(settings.transport))
    else:
        run(
            mcp.run_async(
                settings.transport,
                host=settings.host,
                port=settings.port,
                path=settings.path,
            )
        )

    return 0
