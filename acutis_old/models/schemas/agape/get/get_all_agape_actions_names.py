from typing import List
from pydantic import BaseModel


class AgapeActionNameSchema(BaseModel):
    id: int
    nome: str

    class Config:
        orm_mode = True


class GetAllAgapeActionsNamesResponse(BaseModel):
    acoes_agape: List[AgapeActionNameSchema]
