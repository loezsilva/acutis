import json
from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic_core import PydanticCustomError
from spectree import BaseFile

from acutis_api.communication.enums.vocacional import (
    AprovacaoEnum,
    GeneroVocacionalEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.communication.schemas.vocacional import (
    FormFichaVocacionalSchema,
)


class RegistrarPreCadastroRequest(BaseModel):
    nome: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description='Nome do vocacionado',
        strip_whitespace=True,
    )
    email: str = Field(
        ..., description='E-mail do vocacionado', strip_whitespace=True
    )
    telefone: str = Field(
        ..., description='Telefone do vocacionado', strip_whitespace=True
    )
    genero: GeneroVocacionalEnum = Field(
        ..., description='Gênero do vocacionado', strip_whitespace=True
    )
    pais: str = Field(
        ..., description='País do vocacionado', strip_whitespace=True
    )


class ListarPreCadastrosQuery(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pais: Optional[str] = Field(None, description='Pais')
    pagina: int = Field(None, description='Pagina atual')
    por_pagina: int = Field(None, description='Quantidade por pagina')
    nome: Optional[str] = Field(None, description='Nome vocacional')
    telefone: Optional[str] = Field(None, description='Telefone vocacional')
    email: Optional[str] = Field(
        None, description='Email do Usuario vocacional'
    )
    status: Optional[str] = Field(None, description='Status do vocacional')
    data_final: Optional[str] = Field(None, description='Data  final')
    data_inicial: Optional[str] = Field(None, description='Data  inicial')
    criado_em: Optional[str] = Field(
        None, description='Data de criação do pré cadastro'
    )
    genero: Optional[str] = Field(None, description='Gênero do vocacional')


class AtualizarAndamentoVocacionalRequest(BaseModel):
    usuario_vocacional_id: UUID = Field(
        ..., description='Id do usuário vocacioal'
    )
    acao: AprovacaoEnum = Field(..., description='Ação de aprovar ou recusar')
    justificativa: Optional[str] = Field(
        None, description='Justificativa da ação'
    )


class RegistrarCadastroVocacionalRequest(BaseModel):
    fk_usuario_vocacional_id: UUID = Field(
        ..., description='Id usuário vocacional'
    )
    documento_identidade: str = Field(
        ..., description='Número de identificação pessoal'
    )
    data_nascimento: date = Field(..., description='Data de nascimento')
    codigo_postal: Optional[str] = Field(
        None, description='Cep para brasileiro ou zip_code caso estrangeiro'
    )
    logradouro: Optional[str] = Field(None, description='Logradouro')
    tipo_logradouro: Optional[str] = Field(
        None, description='Tipo de logradouro'
    )
    pais: Optional[str] = Field(None, description='País onde vive')
    numero: Optional[str] = Field(None, description='Número da residência')
    complemento: Optional[str] = Field(
        None, description='Complemento residêncial'
    )
    bairro: Optional[str] = Field(None, description='Bairro')
    cidade: Optional[str] = Field(None, description='Cidade onde reside')
    estado: Optional[str] = Field(
        None, description='Estado onde reside', min_length=2, max_length=2
    )


class ListarCadastrosVocacionaisQuery(BaseModel):
    pagina: int = Field(None, description='Página atual')
    por_pagina: int = Field(None, description='Quantidade por página')
    documento_identidade: Optional[str] = Field(
        None, description='Número de documento'
    )
    email: Optional[str] = Field(None, description='Email vocacional')
    criado_em: Optional[str] = Field(
        None, description='Data de preenchimento do cadastro'
    )
    nome: Optional[str] = Field(None, description='Nome vocacional')
    status: Optional[PassosVocacionalStatusEnum] = Field(
        None, description='Status do cadastro vocacional'
    )
    genero: Optional[GeneroVocacionalEnum] = Field(
        None, description='Gênero masculino ou feminino'
    )
    pais: Optional[str] = Field(None, description='Pais')
    telefone: Optional[str] = Field(None, description='Telefone do vocacioal')
    data_inicial: Optional[str] = Field(None, description='Data Inicial')
    data_final: Optional[str] = Field(None, description='Data Final')
    telefone: Optional[str] = Field(None, description='Telefone do vocacioal')


class RegistrarFichaVocacionalFormData(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    ficha_vocacional: FormFichaVocacionalSchema
    foto_vocacional: BaseFile

    @model_validator(mode='before')
    @classmethod
    def validar_formdata(cls, form_data: dict):
        if 'ficha_vocacional' in form_data and isinstance(
            form_data['ficha_vocacional'], str
        ):
            try:
                form_data['ficha_vocacional'] = json.loads(
                    form_data['ficha_vocacional']
                )
            except json.JSONDecodeError:
                raise PydanticCustomError(
                    'value_error',
                    'O campo "ficha_vocacional" deve ser um JSON válido.',
                )
        return form_data


class ListarFichasVocacionaisQuery(BaseModel):
    pais: Optional[str] = Field(None, description='Pais do vocacional')
    status: Optional[PassosVocacionalStatusEnum] = Field(
        None, description='Status'
    )
    genero: Optional[GeneroVocacionalEnum] = Field(
        None, description='Gênero masculino ou feminino'
    )
    email: Optional[str] = Field(None, description='Email vocacional')
    nome: Optional[str] = Field(None, description='Nome do vocacionanal')
    documento_identidade: str = Field(
        None, description='Documento de idetidade'
    )
    data_inicial: str = Field(None, description='Data filtro de inicio')
    data_final: str = Field(None, description='Data filtro final')
    fk_usuario_vocacional_id: UUID = Field(
        None, description='ID usuário vocacional'
    )
    telefone: Optional[str] = Field(None, description='Telefone do vocacional')
    pagina: Optional[int] = Field(None, description='Pagina')
    por_pagina: Optional[int] = Field(None, description='Por pagina')


class ListarDesistenciaVocacionaisQuery(BaseModel):
    pagina: int = Field(None, description='Página atual')
    por_pagina: int = Field(None, description='Quantidade por página')
    telefone: str = Field(None, description='Telefone do vocacional')
    nome: str = Field(None, description='Nome do vocacional')
    email: str = Field(None, description='Email do vocacional')
    desistencia_em: str = Field(None, description='Data da desistência')
    etapa: str = Field(None, description='Etapa a qual desistiu')
    pais: str = Field(None, description='País onde reside')
    data_inicial: str = Field(None, description='Data inicial')
    data_final: str = Field(None, description='Data final')
    genero: str = Field(None, description='Gênero vocacional')
    status: str = Field(None, description='Status vocacional')
    documento_identidade: str = Field(
        None, description='Documento de identidade'
    )


class ListarVocacionaisRecusadosQuery(BaseModel):
    data_inicial: str = Field(None, description='Data inicial')
    data_final: str = Field(None, description='Data final')
    nome: str = Field(None, description='Nome do vocacional')
    email: str = Field(None, description='Email do vocacional')
    desistencia_em: str = Field(None, description='Data da desistência')
    etapa: str = Field(None, description='Etapa a qual desistiu')
    pais: str = Field(None, description='País onde reside')
    pagina: int = Field(None, description='Pagina')
    por_pagina: int = Field(None, description='Por Pagina')
    pais: str = Field(None, description='Pais')
    telefone: str = Field(None, description='Telefone vocacional')
    genero: str = Field(None, description='Gênero vocacional')
    documento_identidade: str = Field(
        None, description='Documento de identidade'
    )


class RenviarEmailVocacionalRequest(BaseModel):
    usuario_vocacional_id: UUID = Field(..., description='ID vocacional')
