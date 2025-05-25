from typing import List, Optional
from pydantic import BaseModel

from models.agape.instancia_acao_agape import StatusAcaoAgapeEnum
from models.schemas.default import PaginationQuery


class GetAllAgapeActionsInstancesQuery(PaginationQuery):
    fk_acao_agape_id: Optional[int] = None
    status: Optional[StatusAcaoAgapeEnum] = None


class AgapeActionInstanceSchema(BaseModel):
    id: int
    nome_acao_agape: str
    status: StatusAcaoAgapeEnum

    class Config:
        orm_mode = True


class GetAllAgapeActionsInstancesResponse(BaseModel):
    page: int
    total: int
    ciclos: List[AgapeActionInstanceSchema]
