from enum import Enum
from pydantic import BaseModel


class FilterTypesEnum(str, Enum):
    FREQUENCIA = "frequencia"
    VALOR = "valor"


class DonationTypesEnum(str, Enum):
    AVULSA = "avulsa"
    RECORRENTE = "recorrente"


class GetTopRegularDonorsQueryFilter(BaseModel):
    tipo_ordenacao: FilterTypesEnum = FilterTypesEnum.FREQUENCIA
    tipo_doacao: DonationTypesEnum | None = None
    fk_campanhas_ids: str | None = None
    quantidade_meses: int | None = 6
    limite_top_doadores: int | None = 10


class TopRegularDonorSchema(BaseModel):
    nome: str
    fk_usuario_id: int | None
    avatar: str | None

    class Config:
        orm_mode = True


class GetTopRegularDonorsResponse(BaseModel):
    top_doadores: list[TopRegularDonorSchema]
