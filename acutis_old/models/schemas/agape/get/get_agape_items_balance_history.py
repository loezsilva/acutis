from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

from models.agape.historico_movimentacao_agape import TipoMovimentacaoEnum
from models.schemas.default import PaginationQuery
from utils.functions import get_current_time


class GetAgapeItemsBalanceHistoryQuery(PaginationQuery):
    fk_estoque_agape_id: Optional[int] = Field(None, gt=0)
    tipo_movimentacao: Optional[TipoMovimentacaoEnum] = None
    data_movimentacao_inicial: Optional[date] = None
    data_movimentacao_final: Optional[date] = get_current_time().date()


class ItemBalanceHistorySchema(BaseModel):
    id: int
    item: str
    quantidade: int
    tipo_movimentacao: TipoMovimentacaoEnum
    data_movimentacao: str

    class Config:
        orm_mode = True


class GetAgapeItemsBalanceHistoryResponse(BaseModel):
    total: int
    page: int
    movimentacoes: list[ItemBalanceHistorySchema]
