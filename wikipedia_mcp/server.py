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
    The MCP server provides access to Wikipedia content.
    Call search() to find articles by keyword.
    Call fetch() to retrieve the content of a specific article by its page ID.
    """,
    version='1.0.0',
)


@mcp.tool()
async def search(
    keyword: Annotated[str, Field(description='The keyword to search for')],
    language: Annotated[str, Field(description='The language to search in')] = 'en',
) -> SearchResponse | None:
    """
    Search Wikipedia for a keyword in a specified language.
    Returns a list of search results with page IDs, titles, and summaries.

    :param keyword: The keyword to search for.
    :param language: The language to search in (default is 'en' for English).
    :return: A SearchResponse containing a list of SearchItem objects.

    :raises httpx.HTTPStatusError: If the request fails or returns an error status.
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
    id: Annotated[int, Field(description='The page ID to fetch content for')],
    language: Annotated[str, Field(description='The language to fetch in')],
) -> str | None:
    """
    Fetch the content of a Wikipedia page by its ID in a specified language.

    This function retrieves the full HTML content of a Wikipedia page by its page ID.
    It uses the MediaWiki API to fetch the content and returns it as a string.
    The content is normalized to ensure consistent Unicode representation.

    :param id: The page ID of the Wikipedia article to fetch.
    :param language: The language of the Wikipedia article (e.g., 'en' for English).
    :return: The content of the article as a string, or None if not found.

    :raises KeyError: If the 'parse' or 'text' keys are not present in the response.
    :raises httpx.HTTPStatusError: If the request fails or returns an error status.
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
