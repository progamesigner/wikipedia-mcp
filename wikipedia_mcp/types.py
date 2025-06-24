from typing import Annotated

from pydantic import BaseModel, Field, RootModel


class SearchItem(BaseModel):
    id: Annotated[int, Field(..., description='Page ID of the page')]
    title: Annotated[str, Field(..., description='Title of the page')]
    summary: Annotated[str, Field(..., description='Summary of the page')]


class SearchResponse(RootModel[list[SearchItem]]):
    root: Annotated[list[SearchItem], Field(description='List of search results')]
