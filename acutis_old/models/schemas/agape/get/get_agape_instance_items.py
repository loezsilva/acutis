from typing import List
from pydantic import BaseModel


class AgapeInstanceItemSchema(BaseModel):
    fk_item_instancia_agape_id: int
    item: str
    quantidade: int

    class Config:
        orm_mode = True


class GetAgapeInstanceItemsResponse(BaseModel):
    itens_ciclo_agape: List[AgapeInstanceItemSchema]
