from typing import List, Optional

from pydantic import BaseModel, Field

from models.agape.instancia_acao_agape import AbrangenciaInstanciaAcaoAgapeEnum


class AgapeActionAddressSchema(BaseModel):
    cep: Optional[str] = Field(None, max_length=9)
    rua: Optional[str] = Field(None, max_length=100)
    bairro: Optional[str] = Field(None, max_length=80)
    cidade: Optional[str] = Field(None, max_length=32)
    estado: Optional[str] = Field(None, max_length=2)
    numero: Optional[str] = Field(None, max_length=8)
    complemento: Optional[str] = Field(None, max_length=60)


class DonationSchema(BaseModel):
    fk_estoque_agape_id: int = Field(..., gt=0)
    quantidade: int = Field(..., gt=0)


class UpdateAgapeActionRequest(BaseModel):
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum
    endereco: AgapeActionAddressSchema
    doacoes: List[DonationSchema]
