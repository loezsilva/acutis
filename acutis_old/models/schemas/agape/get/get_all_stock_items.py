from typing import List
from pydantic import BaseModel


class StockItemSchema(BaseModel):
    id: int
    item: str
    quantidade: int

    class Config:
        orm_mode = True


class GetAllStockItemsResponse(BaseModel):
    estoques: List[StockItemSchema]
