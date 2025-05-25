import json
import re
import uuid
from datetime import date, datetime
from typing import List, Optional
from uuid import UUID

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
from werkzeug.datastructures import FileStorage

from acutis_api.communication.enums.campanhas import (
    ObjetivosCampanhaEnum,
    TiposCampoEnum,
)
from acutis_api.communication.enums.membros import OrigemCadastroEnum, SexoEnum
from acutis_api.communication.requests.membros import (
    REGEX_NOME,
    CampoAdicionalSchema,
    RegistrarEnderecoMembroSchema,
)


class RegistrarCampanhaSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(..., description='Nome da campanha')
    objetivo: ObjetivosCampanhaEnum = Field(
        ..., description='Objetivo da campanha'
    )
    publica: bool = Field(..., description='Pública ou não')
    ativa: bool = Field(..., description='Ativa ou não')
    meta: Optional[float] = Field(None, description='Meta da campanha')
    chave_pix: Optional[str] = Field(
        None, description='Chave pix caso campanha de doação'
    )
    foto_capa: str = Field(None, description='Filename da imagem de capa')
    fk_cargo_oficial_id: Optional[uuid.UUID] = Field(
        None, description='Requer cargo oficial caso cadastros de oficiais'
    )
    superior_obrigatorio: bool = Field(
        default=False, description='Obriga a preencher superior'
    )


class RegistrarNovaLandingPageSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    conteudo: Optional[str] = Field(
        None, description='Conteúdo da landing page'
    )
    shlink: Optional[str] = Field(None, description='Link encurtado')


class RegistroNovoCampoAdicionalSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome_campo: Optional[str] = Field(
        None, description='Nome do campo adicional caso tenha'
    )
    tipo_campo: TiposCampoEnum = Field(
        None, description='Tipo de dado do campo adicional'
    )
    obrigatorio: Optional[bool] = Field(
        None,
        description='1: Caso o campo obrigatório - 0: Caso não obrigatório',
    )


class RegistrarNovaCampanhaFormData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    dados_da_campanha: RegistrarCampanhaSchema
    foto_capa: Optional[BaseFile]
    dados_da_landing_page: Optional[RegistrarNovaLandingPageSchema]
    campos_adicionais: Optional[List[RegistroNovoCampoAdicionalSchema]]

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        try:
            if 'dados_da_campanha' in form_data and isinstance(
                form_data['dados_da_campanha'], str
            ):
                form_data['dados_da_campanha'] = json.loads(
                    form_data['dados_da_campanha']
                )

            if 'campos_adicionais' in form_data and isinstance(
                form_data['campos_adicionais'], str
            ):
                form_data['campos_adicionais'] = json.loads(
                    form_data['campos_adicionais']
                )
            else:
                form_data['campos_adicionais'] = None

            if 'dados_da_landing_page' in form_data and isinstance(
                form_data['dados_da_landing_page'], str
            ):
                form_data['dados_da_landing_page'] = json.loads(
                    form_data['dados_da_landing_page']
                )
            else:
                form_data['dados_da_landing_page'] = None

            if 'foto_capa' not in form_data or not isinstance(
                form_data['foto_capa'], FileStorage
            ):
                form_data['foto_capa'] = None
            return form_data
        except json.JSONDecodeError:
            raise ValueError('O campos devem conter um JSON válido.')


class ListarCampanhasQuery(BaseModel):
    pagina: Optional[int] = Field(
        default=1,
        description='Número da página atual para paginação.',
    )
    por_pagina: Optional[int] = Field(
        default=10,
        description='Quantidade de itens por página para paginação.',
    )
    id: Optional[UUID] = Field(
        None,
        description='ID único da campanha.',
    )
    nome: Optional[str] = Field(
        None,
        description='Nome da campanha para filtro.',
    )
    objetivo: Optional[ObjetivosCampanhaEnum] = Field(
        None,
        description='Objetivo da campanha para filtro.',
    )
    publica: Optional[int] = Field(
        None,
        description='Campanhas públicas (1) ou privadas (0).',
    )
    ativa: Optional[int] = Field(
        None,
        description='Filtro para campanhas ativas (1) ou inativas (0).',
    )
    data_inicial: Optional[str] = Field(
        None,
        description='Data de criação inicial para filtro (formato: Y-m-d).',
    )
    data_final: Optional[str] = Field(
        None,
        description='Data de criação final para filtro (formato: Y-m-d).',
    )

    ordenar_por: Optional[str] = Field(
        default='desc', description='desc | asc'
    )

    @field_validator('data_inicial', 'data_final')
    def validar_data(cls, value: str) -> str:
        try:
            if value is not None:
                datetime.strptime(value, '%Y-%m-%d')
            return value
        except ValueError:
            raise ValueError("A data deve estar no formato 'Y-m-d'")


class CadastroPorCampanhaFormData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str | None = None
    nome_social: str | None = None
    email: EmailStr | None = None
    numero_documento: str | None = None
    pais: str | None = None
    telefone: str | None = None
    data_nascimento: date | None = None
    sexo: SexoEnum | None = None
    origem_cadastro: OrigemCadastroEnum | None = None
    senha: str | None = None
    foto: BaseFile | None = None
    superior: UUID | None = None
    endereco: RegistrarEnderecoMembroSchema | None
    campos_adicionais: list[CampoAdicionalSchema] | None = None

    @field_validator('nome', mode='before')
    @classmethod
    def validar_e_formatar_nome(cls, value: str):
        if value is None:
            return None
        if not bool(re.match(REGEX_NOME, value)):
            raise PydanticCustomError(
                'value_error', f'O nome {value} possui caracteres inválidos.'
            )
        if len(value) < 3 or len(value) > 100:  # noqa
            raise PydanticCustomError(
                'value_error', 'O nome deve conter entre 3 e 100 caracteres.'
            )
        return value.title()

    @field_validator('nome_social', mode='before')
    @classmethod
    def validar_e_formatar_nome_social(cls, value: str | None):
        if value is None:
            return None
        if not bool(re.match(REGEX_NOME, value)):
            raise PydanticCustomError(
                'value_error',
                f'O nome social {value} possui caracteres inválidos.',
            )
        return value.title()

    @field_validator('numero_documento', mode='before')
    @classmethod
    def validar_e_formatar_numero_documento(cls, value: str):
        if value is None:
            return None
        if len(value) < 11 or len(value) > 50:  # noqa
            raise PydanticCustomError(
                'value_error',
                'O documento deve conter entre 11 e 50 caracteres.',
            )
        return ''.join(filter(str.isdigit, value))

    @field_validator('telefone')
    @classmethod
    def formatar_telefone(cls, value: str):
        if value is None:
            return None
        return ''.join(filter(str.isdigit, value))

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        form_data['nome'] = cls._validate_string_field(form_data, 'nome')
        form_data['nome_social'] = cls._validate_string_field(
            form_data, 'nome_social'
        )
        form_data['email'] = cls._validate_string_field(form_data, 'email')
        form_data['numero_documento'] = cls._validate_string_field(
            form_data, 'numero_documento'
        )
        form_data['pais'] = cls._validate_string_field(form_data, 'pais')
        form_data['telefone'] = cls._validate_string_field(
            form_data, 'telefone'
        )
        form_data['data_nascimento'] = cls._validate_string_field(
            form_data, 'data_nascimento'
        )
        form_data['sexo'] = cls._validate_string_field(form_data, 'sexo')
        form_data['origem_cadastro'] = cls._validate_string_field(
            form_data, 'origem_cadastro'
        )
        form_data['superior'] = cls._validate_string_field(
            form_data, 'superior'
        )
        form_data['endereco'] = cls._validate_json_field(form_data, 'endereco')
        form_data['campos_adicionais'] = cls._validate_json_field(
            form_data, 'campos_adicionais'
        )
        form_data['foto'] = cls._validate_file_field(form_data, 'foto')
        form_data['senha'] = cls._validate_string_field(form_data, 'senha')
        return form_data

    @staticmethod
    def _validate_json_field(form_data: dict, field_name: str):
        if field_name in form_data and isinstance(form_data[field_name], str):
            try:
                return json.loads(form_data[field_name])
            except json.JSONDecodeError:
                raise ValueError(
                    f'O campo "{field_name}" deve ser um JSON válido.'
                )
        return None

    @staticmethod
    def _validate_file_field(form_data: dict, field_name: str):
        if field_name not in form_data or not isinstance(
            form_data[field_name], FileStorage
        ):
            return None
        return form_data[field_name]

    @staticmethod
    def _validate_string_field(form_data: dict, field_name: str):
        if field_name not in form_data or not isinstance(
            form_data[field_name], str
        ):
            return None
        return form_data[field_name]
