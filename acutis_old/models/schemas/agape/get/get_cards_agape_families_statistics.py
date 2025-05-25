from typing import Optional
from pydantic import BaseModel


class GetCardsAgapeFamiliesStatisticsResponse(BaseModel):
    familias_cadastradas: Optional[str]
    renda_media: Optional[str]
    membros_por_familia: Optional[str]
    familias_ativas: Optional[str]
    familias_inativas: Optional[str]
