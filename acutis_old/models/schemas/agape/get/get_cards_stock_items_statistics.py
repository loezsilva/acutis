from typing import Optional
from pydantic import BaseModel


class GetCardsStockItemsStatisticsResponse(BaseModel):
    itens_em_estoque: Optional[str]
    ultima_acao: Optional[str]
    ultima_entrada: Optional[str]
