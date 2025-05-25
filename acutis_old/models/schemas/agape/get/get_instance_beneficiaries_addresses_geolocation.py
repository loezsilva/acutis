from typing import List, Optional
from pydantic import BaseModel


class GeolocationSchema(BaseModel):
    latitude: float
    longitude: float
    latitude_nordeste: float
    longitude_nordeste: float
    latitude_sudoeste: float
    longitude_sudoeste: float

    class Config:
        orm_mode = True


class BeneficiariesGeolocationsSchema(BaseModel):
    nome_familia: str
    latitude: Optional[float]
    longitude: Optional[float]

    class Config:
        orm_mode = True


class GetInstanceBeneficiariesAddressesGeolocationResponse(BaseModel):
    ciclo_acao_agape: GeolocationSchema
    beneficiarios: List[BeneficiariesGeolocationsSchema]
