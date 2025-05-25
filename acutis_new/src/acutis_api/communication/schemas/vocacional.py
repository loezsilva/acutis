from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from acutis_api.communication.enums.vocacional import (
    EstadoCivilEnum,
    GeneroVocacionalEnum,
    PassosVocacionalStatusEnum,
)


class BuscaPreCadastroSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nome: str
    email: str
    telefone: str
    criado_em: str
    genero: str
    status: str
    pais: str
    responsavel_id: Optional[UUID]
    responsavel: Optional[str]

    @field_validator('criado_em', mode='before')
    def parse_data_criacao(cls, value):
        if isinstance(value, datetime):
            return value.strftime('%d/%m/%Y %H:%M:%S')
        return value


class FormFichaVocacionalSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    sacramentos: list = Field(..., description='Sacramentos realizados.')
    motivacao_instituto: str = Field(
        ..., description='Motivação por escolher o instituto.'
    )
    fk_usuario_vocacional_id: UUID = Field(
        ..., description='ID usuário_vocacional'
    )
    motivacao_admissao_vocacional: str = Field(
        ..., description='Motivação pelo processo vocacional'
    )
    referencia_conhecimento_instituto: str = Field(
        ..., description='Como conheceu o instituto'
    )
    identificacao_instituto: str = Field(
        ..., description='Pontos de identificação com o instituto'
    )
    seminario_realizado_em: date = Field(
        ..., description='Data de realização do seminário'
    )
    testemunho_conversao: str = Field(
        ..., description='Testemunho de conversão'
    )
    escolaridade: str = Field(..., description='Escolaridade')
    profissao: str = Field(..., description='Profissão')
    cursos: Optional[str] = Field(None, description='Cursos e formações')
    rotina_diaria: str = Field(..., description='Rotina diária')
    aceitacao_familiar: str = Field(..., description='Aceitação familiar')
    estado_civil: EstadoCivilEnum = Field(None, description='Estado civíl')
    motivo_divorcio: Optional[str] = Field(
        None, description='Motivo do divórcio'
    )
    deixou_religiao_anterior_em: Optional[date] = Field(
        None, description='Data que deixou a última religião'
    )
    remedio_controlado_inicio: Optional[date] = Field(
        None, description='Data que iniciou a tomar rémedio controlado'
    )
    remedio_controlado_termino: Optional[date] = Field(
        None, description='Data que finalizou o uso de rémedio controlado'
    )
    descricao_problema_saude: Optional[str] = Field(
        None, description='Problema de saúde'
    )


class FichaVocacionalResponseSchema(BaseModel):
    sacramentos: list
    status: str
    motivacao_instituto: str
    usuario_vocacional_id: UUID
    motivacao_admissao_vocacional: str
    referencia_conhecimento_instituto: str
    identificacao_instituto: str
    seminario_realizado_em: str
    testemunho_conversao: str
    escolaridade: str
    profissao: str
    cursos: Optional[str]
    rotina_diaria: str
    aceitacao_familiar: str
    estado_civil: EstadoCivilEnum
    motivo_divorcio: Optional[str]
    deixou_religiao_anterior_em: Optional[str]
    remedio_controlado_inicio: Optional[str]
    remedio_controlado_termino: Optional[str]
    descricao_problema_saude: Optional[str]
    foto_vocacional: str
    responsavel_id: Optional[UUID]
    responsavel: Optional[str]


class CadastroVocacionalSchema(BaseModel):
    id: UUID = Field(..., description='ID do cadastro vocacional')
    usuario_vocacional_id: UUID = Field(
        ..., description='ID usuário vocacional'
    )
    nome: str = Field(..., description='Nome vocacional')
    documento_identidade: str = Field(
        ..., description='Documento de identificação'
    )
    criado_em: str = Field(..., description='Data da criação do cadastro')
    email: str = Field(..., description='Email do vocacional')
    data_nascimento: str = Field(..., description='Data de nascimento')
    status: PassosVocacionalStatusEnum = Field(
        ..., description='Status do cadastro'
    )
    genero: GeneroVocacionalEnum = Field(
        ..., description='Gênero do vocacional'
    )
    logradouro: Optional[str] = Field(None, description='Logradouro')
    cidade: Optional[str] = Field(None, description='Cidade onde reside')
    bairro: Optional[str] = Field(None, description='Bairro onde reside')
    estado: Optional[str] = Field(None, description='Estado onde reside')
    numero: Optional[str] = Field(None, description='Número da residência')
    codigo_postal: Optional[str] = Field(None, description='Codigo Postal')
    pais: str = Field(..., description='País onde reside')
    tipo_logradouro: Optional[str] = Field(
        None, description='Tipo de logradouro'
    )
    telefone: str = Field(..., description='Telefone do vocacional')
    responsavel: Optional[str] = Field(
        None,
        description='Nome do responsável por aprovar ou recusar vocacional',
    )
    responsavel_id: Optional[UUID] = Field(
        None, description='Responsável por aprovar ou recusar vocacional'
    )
    complemento: Optional[str] = Field(
        None, description='Complemento endereço'
    )


class BuscaCadastroVocacionalSchema(BaseModel):
    id: UUID
    nome: str
    documento_identidade: str
    criado_em: str
    email: str
    data_nascimento: str
    status: PassosVocacionalStatusEnum
    genero: GeneroVocacionalEnum
    logradouro: str | None
    cidade: str | None
    bairro: str | None
    estado: str | None
    numero: str | None
    codigo_postal: str | None
    pais: str
    tipo_logradouro: str | None
    telefone: str
    responsavel: str | None
    responsavel_id: UUID | None
    complemento: str | None


class ListarVocacionalSchema(BaseModel):
    pre_cadastro: BuscaPreCadastroSchema
    cadastro_vocacional: BuscaCadastroVocacionalSchema | dict
    ficha_do_vocacional: FichaVocacionalResponseSchema | dict


class ListarDesistenciasVocacionaisSchema(BaseModel):
    usuario_vocacional_id: UUID
    nome: str
    genero: GeneroVocacionalEnum
    email: str
    desistencia_em: str
    etapa: str
    pais: str
    telefone: str


class ListarVocacionaisRecusadosSchema(BaseModel):
    justificativa: str | None
    nome: str
    genero: GeneroVocacionalEnum
    email: str
    reprovado_em: str
    etapa: str
    pais: str
    responsavel: str | None
    usuario_vocacional_id: UUID
    telefone: str
