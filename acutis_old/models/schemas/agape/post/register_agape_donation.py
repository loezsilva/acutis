from typing import List
from pydantic import BaseModel, Field

from utils.response import DefaultResponseSchema


class DonatedItemsSchema(BaseModel):
    fk_item_instancia_agape_id: int = Field(..., gt=0)
    quantidade: int = Field(..., gt=0)


class RegisterAgapeDonationRequest(BaseModel):
    fk_familia_agape_id: int = Field(..., gt=0)
    fk_instancia_acao_agape_id: int = Field(..., gt=0)
    doacoes: List[DonatedItemsSchema] = Field(..., min_items=1)


class RegisterAgapeDonationResponse(DefaultResponseSchema):
    fk_doacao_agape_id: int
