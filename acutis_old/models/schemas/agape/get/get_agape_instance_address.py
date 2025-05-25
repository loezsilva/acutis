from typing import Optional
from pydantic import BaseModel

from models.agape.instancia_acao_agape import AbrangenciaInstanciaAcaoAgapeEnum


class GetAgapeInstanceAddressResponse(BaseModel):
    cep: Optional[str]
    rua: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    abrangencia: AbrangenciaInstanciaAcaoAgapeEnum
