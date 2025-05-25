import json
import re
import uuid
from datetime import date
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)
from pydantic_core import PydanticCustomError
from spectree import BaseFile

from acutis_api.communication.enums.membros import (
    OrigemCadastroEnum,
    SexoEnum,
)

REGEX_NOME = r'^[a-zA-ZáÁâÂãÃàÀéÉêÊèÈíÍóÓôÔõÕúÚùÙçÇ\s]+$'


class RegistrarMembroSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(..., min_length=3, max_length=100)
    nome_social: str
    email: EmailStr
    numero_documento: str
    telefone: str
    data_nascimento: date
    sexo: SexoEnum
    origem_cadastro: OrigemCadastroEnum

    @field_validator('nome', mode='before')
    @classmethod
    def validar_e_formatar_nome(cls, value: str):
        if not bool(re.match(REGEX_NOME, value)):
            raise PydanticCustomError(
                'value_error', f'O nome {value} possui caracteres inválidos.'
            )
        if len(value) < 3 or len(value) > 100:  # noqa
            raise PydanticCustomError(
                'value_error', 'O nome deve conter entre 3 e 100 caracteres.'
            )
        return value.title()

    @field_validator('nome_social')
    @classmethod
    def validar_e_formatar_nome_social(cls, value: str):
        if not bool(re.match(REGEX_NOME, value)):
            raise PydanticCustomError(
                'value_error',
                f'O nome social {value} possui caracteres inválidos.',
            )
        return value.title()

    @field_validator('numero_documento')
    @classmethod
    def validar_e_formatar_numero_documento(cls, value: str):
        if len(value) < 11 or len(value) > 50:  # noqa
            raise PydanticCustomError(
                'value_error',
                'O documento deve conter entre 11 e 50 caracteres.',
            )
        return ''.join(filter(str.isdigit, value))

    @field_validator('telefone')
    @classmethod
    def formatar_telefone(cls, value: str):
        return ''.join(filter(str.isdigit, value))


class RegistrarEnderecoMembroSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    codigo_postal: str
    tipo_logradouro: str | None = None
    logradouro: str
    numero: str | None = None
    complemento: str | None = None
    bairro: str | None = None
    cidade: str
    estado: str | None = None
    pais: str

    @field_validator('codigo_postal')
    @classmethod
    def formatar_codigo_postal(cls, value: str):
        return ''.join(filter(str.isdigit, value))

    @field_validator('estado', mode='after')
    @classmethod
    def validar_estado(cls, value: str | None):
        if not value:
            return value

        if len(value) != 2:  # noqa
            raise PydanticCustomError(
                'value_error',
                'O campo "Estado" deve conter exatamente 2 caracteres.',
            )
        return value.upper()


class RegistrarNovoMembroFormData(BaseModel):
    membro: RegistrarMembroSchema
    endereco: RegistrarEnderecoMembroSchema
    foto: BaseFile | None = None
    campanha_id: uuid.UUID | None = None

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        if 'membro' in form_data and isinstance(form_data['membro'], str):
            try:
                form_data['membro'] = json.loads(form_data['membro'])
            except json.JSONDecodeError:
                raise PydanticCustomError(
                    'value_error', 'O campo "membro" deve ser um JSON válido.'
                )

        if 'endereco' in form_data and isinstance(form_data['endereco'], str):
            try:
                form_data['endereco'] = json.loads(form_data['endereco'])
            except json.JSONDecodeError:
                raise PydanticCustomError(
                    'value_error',
                    'O campo "endereco" deve ser um JSON válido.',
                )
        return form_data


class CampoAdicionalSchema(BaseModel):
    campo_adicional_id: uuid.UUID
    valor_campo: Any


class RegistrarNovoLeadRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str
    email: EmailStr
    telefone: str
    pais: str
    campanha_id: uuid.UUID | None = None
    origem_cadastro: OrigemCadastroEnum
    campos_adicionais: list[CampoAdicionalSchema] | None = None

    @field_validator('nome')
    @classmethod
    def validar_e_formatar_nome(cls, value: str):
        if not bool(re.match(REGEX_NOME, value)):
            raise PydanticCustomError(
                'value_error', f'O nome {value} possui caracteres inválidos.'
            )
        if len(value) > 100:  # noqa
            raise PydanticCustomError(
                'value_error', 'O nome deve conter no máximo 100 caracteres.'
            )
        return value.title()

    @field_validator('telefone')
    @classmethod
    def formatar_telefone(cls, value: str):
        return ''.join(filter(str.isdigit, value))
