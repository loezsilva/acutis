from typing import Optional
from pydantic import BaseModel


class GetFamilyAddressByIdResponse(BaseModel):
    id: int
    rua: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    ponto_referencia: Optional[str]
    bairro: Optional[str]
    cidade: Optional[str]
    estado: Optional[str]
    cep: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        orm_mode = True
