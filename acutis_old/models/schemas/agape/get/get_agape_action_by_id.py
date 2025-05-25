from typing import List, Optional
from pydantic import BaseModel

from models.agape.instancia_acao_agape import AbrangenciaInstanciaAcaoAgapeEnum


class AgapeActionAddressSchema(BaseModel):
    cep: Optional[str]
    rua: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]

    class Config:
        orm_mode = True


class DonationSchema(BaseModel):
    fk_estoque_agape_id: int
    item: str
    quantidade: int

    class Config:
        orm_mode = True


class GetAgapeActionByIdResponse(BaseModel):
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum
    endereco: AgapeActionAddressSchema
    doacoes: List[DonationSchema]
