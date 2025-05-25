from typing import List, Optional
from pydantic import BaseModel


class AgapeFamilyAddress(BaseModel):
    cep: str
    rua: str
    numero: Optional[str]
    complemento: Optional[str]
    ponto_referencia: Optional[str]
    bairro: str
    cidade: str
    estado: str
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        orm_mode = True


class GetAllAgapeFamiliesAddressResponse(BaseModel):
    enderecos: List[AgapeFamilyAddress]
