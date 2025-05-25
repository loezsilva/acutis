from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

from models.schemas.default import PaginationQuery
from utils.functions import get_current_time


class ReceiptsEnum(str, Enum):
    com_recibo = "com_recibo"
    sem_recibo = "sem_recibo"


class GetBeneficiariesByAgapeActionIdQuery(PaginationQuery):
    cpf: Optional[str] = Field(None, max_length=14)
    data_inicial: Optional[date] = Field(None)
    data_final: Optional[date] = Field(get_current_time().date())
    recibos: Optional[ReceiptsEnum] = Field(None)


class BeneficiariesSchema(BaseModel):
    fk_doacao_agape_id: int
    nome_familia: str
    data_hora_doacao: str
    recibos: Optional[list[str]]

    class Config:
        orm_mode = True


class GetBeneficiariesByAgapeActionIdResponse(BaseModel):
    page: int
    total: int
    beneficiarios: list[BeneficiariesSchema]
