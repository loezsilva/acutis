from datetime import date
from typing import List, Optional
from pydantic import BaseModel

from models.schemas.default import PaginationQuery
from utils.functions import get_current_time


class GetAllAgapeActionsQuery(PaginationQuery):
    fk_acao_agape_id: Optional[int] = None
    data_cadastro_inicial: Optional[date] = None
    data_cadastro_final: Optional[date] = get_current_time().date()


class AgapeActionSchema(BaseModel):
    id: int
    nome: str
    data_cadastro: str
    ciclos_finalizados: int

    class Config:
        orm_mode = True


class GetAllAgapeActionsResponse(BaseModel):
    page: int
    total: int
    acoes_agape: List[AgapeActionSchema]
