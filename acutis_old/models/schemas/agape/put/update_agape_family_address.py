from typing import Optional
from pydantic import BaseModel, Field, constr


class UpdateAgapeFamilyAddressRequest(BaseModel):
    cep: constr(min_length=8, max_length=9, strip_whitespace=True)  # type: ignore
    rua: constr(
        min_length=3, max_length=100, strip_whitespace=True
    )  # type: ignore
    numero: Optional[str] = Field(None, max_length=8)
    complemento: Optional[str] = Field(None, max_length=60)
    ponto_referencia: Optional[str] = Field(None, max_length=100)
    bairro: constr(min_length=3, max_length=80, strip_whitespace=True)  # type: ignore
    cidade: constr(min_length=3, max_length=32, strip_whitespace=True)  # type: ignore
    estado: constr(min_length=2, max_length=2, strip_whitespace=True)  # type: ignore
