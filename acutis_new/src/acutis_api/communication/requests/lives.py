import uuid
from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from acutis_api.communication.enums.lives import (
    DiaSemanaEnum,
    TipoProgramacaoLiveEnum,
)
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class FiltroDiaSemana(BaseModel):
    dia_semana: DiaSemanaEnum = Field(
        ..., description='Dia da semana para filtrar as lives'
    )


class RegistrarCanalRequest(BaseModel):
    tag: str = Field(
        ..., min_length=3, max_length=50, description='Nome do canal'
    )
    rede_social: str = Field(
        ..., min_length=2, max_length=20, description='Rede social do canal'
    )
    campanha_id: uuid.UUID | None = Field(None, description='ID da campanha')

    class Config:
        from_attributes = True


class ObterCanalRequest(BaseModel):
    tag: str = Field(
        None, min_length=3, max_length=50, description='Nome do canal (tag)'
    )
    rede_social: str = Field(
        None, min_length=2, max_length=20, description='Rede social do canal'
    )

    class Config:
        from_attributes = True


class ProgramacaoRecorrenteRequest(BaseModel):
    dia_semana: str
    hora_inicio: time


class RegistrarLiveRequest(BaseModel):
    tipo: TipoProgramacaoLiveEnum
    canais_ids: List[uuid.UUID] = Field(
        ..., description='IDs dos canais que irão transmitir a live'
    )
    data_hora_inicio: Optional[datetime] = Field(
        None, description='Data e hora de início da live avulsa'
    )
    programacoes: Optional[List[ProgramacaoRecorrenteRequest]] = Field(
        None, description='Lista de programações para lives recorrentes'
    )

    @field_validator('programacoes', mode='before')
    @classmethod
    def valida_programacoes(cls, valor):
        if valor is not None and not isinstance(valor, list):
            raise ValueError('programacoes deve ser uma lista')
        return valor

    @classmethod
    def validate(cls, values):
        tipo = values.get('tipo')
        data_hora_inicio = values.get('data_hora_inicio')
        programacoes = values.get('programacoes')

        if tipo == TipoProgramacaoLiveEnum.AVULSA:
            if not data_hora_inicio:
                raise ValueError(
                    "O campo 'data_hora_inicio' é obrigatório p/ lives avulsas"
                )
        elif tipo == TipoProgramacaoLiveEnum.RECORRENTE:
            if not programacoes or len(programacoes) == 0:
                raise ValueError(
                    "O campo 'programacoes' é obrigatório p/ lives recorrentes"
                )
        return values


class ObterLivesProgramadasRequest(BaseModel):
    tipo_programacao: Optional[TipoProgramacaoLiveEnum] = Field(
        None, description='Tipo de programação da live'
    )
    rede_social: Optional[str] = Field(
        None, min_length=2, max_length=20, description='Rede social da live'
    )
    filtro_dias_semana: Optional[List[DiaSemanaEnum]] = Field(
        None, description='Lista de dias da semana para filtrar as lives'
    )


class EditarProgramacaoLiveRequest(BaseModel):
    tipo_programacao: TipoProgramacaoLiveEnum
    data_hora_inicio: Optional[datetime] = Field(
        None, description='Nova data e hora de início'
    )
    hora_inicio: Optional[time] = Field(
        None, description='Hora de início para programação recorrente'
    )
    dia_semana: Optional[DiaSemanaEnum] = Field(
        None, description='Dia da semana para lives periódicas'
    )

    @model_validator(mode='before')
    @classmethod
    def validar_campos_conforme_tipo(cls, values):
        tipo = values.get('tipo_programacao')

        if tipo == TipoProgramacaoLiveEnum.AVULSA and not values.get(
            'data_hora_inicio'
        ):
            raise ValueError(
                "O campo 'data_hora_inicio' é obrigatório para lives avulsas."
            )

        if tipo == TipoProgramacaoLiveEnum.RECORRENTE:
            if not values.get('hora_inicio'):
                raise ValueError(
                    (
                        "O campo 'hora_inicio' é obrigatório "
                        'para lives recorrentes.'
                    )
                )
            if not values.get('dia_semana'):
                raise ValueError(
                    (
                        "O campo 'dia_semana' é obrigatório "
                        'para lives recorrentes.'
                    )
                )

        return values


class DeletarProgramacaoLiveRequest(BaseModel):
    programacao_id: uuid.UUID
    tipo_programacao: TipoProgramacaoLiveEnum


class ObterTodasLivesRecorrentesRequest(PaginacaoQuery):
    tag: Optional[str] = None
    rede_social: Optional[str] = None
    hora_inicio: Optional[str] = None
    dia_semana: Optional[str] = None


class FiltrosLivesRecorrentes(PaginacaoQuery):
    tag: Optional[str] = None
    rede_social: Optional[str] = None
    dia_semana: Optional[str] = None


class ObterTodasLivesAvulsasRequest(PaginacaoQuery):
    tag: Optional[str] = None
    rede_social: Optional[str] = None
    data_hora_inicio: Optional[datetime] = None
    live_id: Optional[uuid.UUID] = None
    campanha_id: Optional[uuid.UUID] = None


class ObterAudienciaLivesRequest(BaseModel):
    live_id: uuid.UUID = Field(..., description='ID da live')
    data_inicial: Optional[date] = Field(
        None, description='Data inicial no formato YYYY-MM-DD'
    )
    data_final: Optional[date] = Field(
        None, description='Data final no formato YYYY-MM-DD'
    )

    @field_validator('data_inicial', 'data_final', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if not v:
            return None
        return v


class ObterHistogramaLiveRequest(BaseModel):
    filtro_titulo_live: str = Field(..., description='Título da live')
    filtro_rede_social: str | None = Field(None, description='Rede social')
