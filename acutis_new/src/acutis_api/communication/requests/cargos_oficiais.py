import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError


class RegistrarCargosOficiaisRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome_cargo: str = Field(..., description='Nome do cargo oficial')
    fk_cargo_superior_id: Optional[uuid.UUID] = Field(
        None, description='ID do cargo superior'
    )

    @field_validator('nome_cargo')
    @classmethod
    def verificar_nome_cargo(cls, value: str):
        if len(value) < 4:  # noqa
            raise PydanticCustomError(
                'value_error', 'Nome do cargo deve ter mínimo de 4 caracteres'
            )
        return value


class ListarCargosOficiaisQuery(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: str = Field(None, description='ID cargo oficial')
    ordenar_por: str = Field(default='desc', description='desc | asc')
    nome_cargo: str = Field(None, description='Nome do cargo oficial')
    pagina: int = Field(default=1, description='Página atual')
    por_pagina: int = Field(default=10, description='Quantidade por página')


class ListarCargosOficiaisSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    id: uuid.UUID
    nome_cargo: str
    criado_em: str
    criado_por: uuid.UUID
    cargo_superior: Optional[str]


class ListarCargosOficiaisResponse(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    cargos: list[ListarCargosOficiaisSchema]
    pagina: int
    paginas: int
    total: int
