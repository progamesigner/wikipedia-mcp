from typing import Annotated
from unicodedata import normalize

from fastmcp import FastMCP
from httpx import AsyncClient
from pydantic import Field

from wikipedia_mcp.types import SearchItem, SearchResponse

BASE_URL_TEMPLATE = r'https://{language}.wikipedia.org/w/api.php'

mcp = FastMCP[None](
    'Wikipedia MCP',
    """
        This server provides data analysis tools.
        Call get_average() to analyze numerical data.
    """,
    version='1.0.0',
)


@mcp.tool()
async def search(
    keyword: Annotated[str, Field()],
    language: Annotated[str, Field(description='The language to search in')] = 'en',
) -> SearchResponse | None:
    """
    Search for a keyword in a specified language. Returns the result of all possible content.
    """
    async with AsyncClient(follow_redirects=True) as client:
        response = await client.get(
            BASE_URL_TEMPLATE.format(language=language),
            params={
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': keyword,
                'converttitles': True,
            },
        )
        data = response.raise_for_status().json()
        return SearchResponse(
            [
                SearchItem(
                    id=item['pageid'],
                    title=item['title'],
                    summary=normalize('NFKD', item['snippet']),
                )
                for item in data['query']['search']
            ]
        )


@mcp.tool()
async def fetch(
    id: Annotated[int, Field()],
    language: Annotated[str, Field(description='The language to fetch in')],
) -> str | None:
    """
    Fetch single page content by ID in a specified language.
    """
    async with AsyncClient(follow_redirects=True) as client:
        response = await client.get(
            BASE_URL_TEMPLATE.format(language=language),
            params={
                'action': 'parse',
                'format': 'json',
                'pageid': id,
                'prop': 'text',
            },
        )
        data = response.raise_for_status().json()
        return normalize('NFKD', data['parse']['text']['*'])
