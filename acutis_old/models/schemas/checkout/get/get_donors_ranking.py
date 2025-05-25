from enum import Enum
from pydantic import BaseModel

from models.schemas.default import PaginationQuery


class DonationTypesEnum(str, Enum):
    AVULSA = "avulsa"
    RECORRENTE = "recorrente"


class GetDonorsRankingQueryFilter(PaginationQuery):
    tipo_doacao: DonationTypesEnum | None = None
    fk_campanhas_ids: str | None = None
    quantidade_meses: int | None = 6


class DonorRankingSchema(BaseModel):
    benfeitor: str
    quantidade_doacoes: int
    valor_total_doacoes: float
    fk_usuario_id: int | None

    class Config:
        orm_mode = True


class GetDonorsRankingResponse(BaseModel):
    total: int
    page: int
    pages: int
    doadores: list[DonorRankingSchema]
