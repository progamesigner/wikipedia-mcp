from asyncio import run

from fastmcp import Client
from mcp.types import ContentBlock, TextContent

from wikipedia_mcp.server import mcp

client = Client(mcp)


async def call(keyword: str, language: str) -> list[ContentBlock]:
    async with client:
        result = await client.call_tool(
            'search',
            {'keyword': keyword, 'language': language},
        )
        return result.content


def test_search() -> None:
    response = run(call('Python', 'en'))

    assert len(response) > 0
    assert all(isinstance(item, TextContent) for item in response)
    assert any(
        isinstance(item, TextContent) and 'Python (programming language)' in item.text
        for item in response
    )


def test_search_zh() -> None:
    response = run(call('Python', 'zh-tw'))

    assert len(response) > 0
    assert all(isinstance(item, TextContent) for item in response)
    assert any(
        isinstance(item, TextContent) and '编程语言' in item.text for item in response
    )


if __name__ == '__main__':
    run(call('Python', 'en'))
    run(call('Python', 'zh-tw'))
