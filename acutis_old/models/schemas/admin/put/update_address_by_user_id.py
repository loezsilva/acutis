from typing import Optional
from pydantic import BaseModel, Field


class UpdateAddressByUserIdRequest(BaseModel):
    cep: Optional[str] = Field(max_length=9)
    rua: Optional[str] = Field(max_length=100)
    numero: Optional[str] = Field(max_length=8)
    complemento: Optional[str] = Field(max_length=60)
    ponto_referencia: Optional[str] = Field(max_length=100)
    bairro: Optional[str] = Field(max_length=80)
    estado: Optional[str] = Field(max_length=2)
    cidade: Optional[str] = Field(max_length=32)
    detalhe_estrangeiro: Optional[str] = Field(
        description="Campo preenchido caso o benfeitor não resida no Brasil."
    )
