from enum import Enum
import json
from typing import Optional
from datetime import date

from pydantic import BaseModel, Field, validator
from spectree import BaseFile


class GenderEnum(str, Enum):
    masculino = "masculino"
    feminino = "feminino"


class UserUpdateSchema(BaseModel):
    nome: str = Field(
        ..., min_length=6, max_length=100, description="Nome completo"
    )
    nome_social: Optional[str] = Field(
        None,
        max_length=45,
        description="Nome que o benfeitor prefere ser chamado",
    )
    data_nascimento: date = Field(
        ..., description="Data de nascimento no formato 'YYYY-MM-DD'"
    )
    telefone: str = Field(
        ...,
        min_length=11,
        max_length=30,
        description="Celular ou telefone do benfeitor",
    )
    sexo: GenderEnum = Field(..., description="Sexo do benfeitor")


class UserAddressUpdateSchema(BaseModel):
    cep: Optional[str] = Field(None, max_length=9)
    rua: Optional[str] = Field(None, max_length=100)
    numero: Optional[str] = Field(None, max_length=8)
    complemento: Optional[str] = Field(None, max_length=60)
    bairro: Optional[str] = Field(None, max_length=80)
    estado: Optional[str] = Field(None, max_length=2)
    cidade: Optional[str] = Field(None, max_length=32)
    detalhe_estrangeiro: Optional[str] = Field(
        None,
        description="Campo preenchido caso o benfeitor não resida no Brasil.",
    )


class UpdateUserRequest(BaseModel):
    usuario: UserUpdateSchema
    endereco: UserAddressUpdateSchema


class UpdateUserFormData(BaseModel):
    image: Optional[BaseFile] = Field(
        None, description="Imagem do usuário enviada como arquivo"
    )
    data: str = Field(
        ...,
        description="""
                        {
                            "endereco": {
                                "bairro": "string",
                                "cep": "string",
                                "cidade": "string",
                                "complemento": "string",
                                "detalhe_estrangeiro": "string",
                                "estado": "st",
                                "numero": "string",
                                "rua": "string"
                            },
                            "usuario": {
                                "data_nascimento": "2024-12-03",
                                "nome": "string",
                                "nome_social": "string",
                                "sexo": "string",
                                "telefone": "stringstrin"
                            }
                        }
                    """,
    )

    @validator("data", pre=True)
    def parse_data(cls, value):
        try:
            parsed_data = json.loads(value)
            UpdateUserRequest.parse_obj(parsed_data)
            return value
        except Exception as e:
            raise ValueError(f"Erro ao validar o campo 'data': {e}")
