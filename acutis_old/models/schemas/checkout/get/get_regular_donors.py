from enum import Enum

from pydantic import BaseModel, Field
from models.schemas.default import PaginationQuery, PaginationResponse


class DonationTypesEnum(str, Enum):
    AVULSA = "avulsa"
    RECORRENTE = "recorrente"


class GetRegularDonorsQueryFilter(PaginationQuery):
    tipo_doacao: DonationTypesEnum | None = None
    fk_campanhas_ids: str | None = None
    quantidade_meses: int | None = Field(6, ge=1, le=13)


class RegularDonorSchema(BaseModel):
    benfeitor: str
    doacoes: str
    fk_usuario_id: int | None
    meses: dict[str, bool]


class GetRegularDonorsResponse(PaginationResponse):
    doadores_assiduos: list[RegularDonorSchema]
