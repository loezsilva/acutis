from datetime import date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, SecretStr, constr


class GenderEnum(str, Enum):
    masculino = "masculino"
    feminino = "feminino"


class UserSchema(BaseModel):
    nome: constr(min_length=6, max_length=100, strip_whitespace=True)  # type: ignore
    email: constr(min_length=6, max_length=60, strip_whitespace=True)  # type: ignore
    cpf: constr(min_length=11, max_length=14, strip_whitespace=True)  # type: ignore
    data_nascimento: date
    telefone: constr(min_length=11, max_length=15, strip_whitespace=True)  # type: ignore
    sexo: GenderEnum
    password: SecretStr = Field(..., min_length=8, max_length=16)  # type: ignore
    campanha_origem: Optional[int] = None


class AddressSchema(BaseModel):
    cep: constr(min_length=8, max_length=9, strip_whitespace=True)  # type: ignore
    estado: constr(min_length=2, max_length=2, strip_whitespace=True)  # type: ignore
    cidade: constr(min_length=3, max_length=32, strip_whitespace=True)  # type: ignore
    bairro: constr(min_length=3, max_length=80, strip_whitespace=True)  # type: ignore
    rua: constr(min_length=3, max_length=100, strip_whitespace=True)  # type: ignore
    numero: Optional[str] = Field(None, max_length=8)
    complemento: Optional[str] = Field(None, max_length=60)


class RegisterBrazilianUserWithAddressRequest(BaseModel):
    usuario: UserSchema
    endereco: AddressSchema
