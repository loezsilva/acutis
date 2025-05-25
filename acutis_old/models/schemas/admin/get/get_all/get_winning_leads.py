from typing import Optional
from pydantic import BaseModel, EmailStr


class GetWinningLeadsFilters(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 10
    filtro_acao_id: Optional[int] = None


class GetWinningLeadsSchema(BaseModel):
    id: int
    nome: Optional[str]
    tel: Optional[str]
    email: Optional[EmailStr]
    data_sorteio: Optional[str]
    acao_sorteada: Optional[int]

    class Config:
        orm_mode = True


class GetWinningLeadsResponse(BaseModel):
    page: int
    total: int
    leads_sorteados: list[GetWinningLeadsSchema]
