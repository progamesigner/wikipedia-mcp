from asyncio import run
from typing import Annotated

from fastmcp.server.server import Transport
from pydantic import Field
from pydantic_settings import BaseSettings

from wikipedia_mcp.server import mcp


class Settings(BaseSettings):
    host: Annotated[str | None, Field(alias='SERVE_HOST')] = None
    path: Annotated[str | None, Field(alias='SERVE_PATH')] = None
    port: Annotated[int | None, Field(alias='SERVE_PORT')] = None
    transport: Annotated[Transport, Field()] = 'stdio'


settings = Settings()


def arguments(transport: Transport) -> dict[str, int | str | None]:
    if transport in {'stdio'}:
        return {}
    else:
        return {
            'host': settings.host,
            'port': settings.port,
            'path': settings.path,
        }


def main() -> None:
    run(mcp.run_async(settings.transport, **arguments(settings.transport)))
