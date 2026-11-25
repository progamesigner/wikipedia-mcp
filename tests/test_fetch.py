from asyncio import run

from fastmcp import Client
from mcp.types import ContentBlock, TextContent

from wikipedia_mcp.server import mcp

client = Client(mcp)


async def call(id: int, language: str) -> list[ContentBlock]:
    async with client:
        result = await client.call_tool(
            'fetch',
            {'id': id, 'language': language},
        )
        return result.content


def test_fetch() -> None:
    response = run(call(23862, 'en'))

    assert len(response) > 0
    assert all(isinstance(item, TextContent) for item in response)
    assert any(
        isinstance(item, TextContent)
        and 'Python (programming language)' in item.text
        and 'Guido van Rossum' in item.text
        for item in response
    )


def test_fetch_zh() -> None:
    response = run(call(3881, 'zh-tw'))

    assert len(response) > 0
    assert all(isinstance(item, TextContent) for item in response)
    assert any(
        isinstance(item, TextContent)
        and 'Python (programming language)' in item.text
        and 'Guido van Rossum' in item.text
        for item in response
    )


if __name__ == '__main__':
    run(call(23862, 'en'))
    run(call(3881, 'zh-tw'))
