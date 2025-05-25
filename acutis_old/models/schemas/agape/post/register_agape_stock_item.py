from pydantic import BaseModel, Field


class RegisterAgapeStockItemRequest(BaseModel):
    item: str = Field(..., min_length=3, max_length=100)
