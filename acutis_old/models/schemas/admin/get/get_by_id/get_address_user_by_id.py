from typing import Optional

from pydantic import BaseModel


class GetAddressByUserIdResponse(BaseModel):
    id: int
    cep: Optional[str]
    rua: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    pais_origem: Optional[str]
    detalhe_estrangeiro: Optional[str]

    class Config:
        orm_mode = True
