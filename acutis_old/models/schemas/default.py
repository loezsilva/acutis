from typing import Optional
from pydantic import BaseModel


class PaginationQuery(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 10


class PaginationResponse(BaseModel):
    total: int
    page: int
    pages: int


class DefaultURLResponse(BaseModel):
    url: str
