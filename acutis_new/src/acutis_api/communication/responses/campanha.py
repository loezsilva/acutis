import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, RootModel, model_validator

from acutis_api.communication.enums.campanhas import ObjetivosCampanhaEnum


def formatar_data(data: datetime) -> str:
    return data.strftime('%d/%m/%Y %H:%M:%S')


class RegistrarNovaCampanhaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str


class CampanhaResponse(BaseModel):
    id: uuid.UUID
    objetivo: str
    nome: str
    publica: bool
    ativa: bool
    meta: Optional[float]
    capa: Optional[str]
    chave_pix: Optional[str]
    criado_em: str
    criado_por: uuid.UUID
    atualizado_em: Optional[str]

    @model_validator(mode='before')
    @classmethod
    def formatar_datas(cls, data: dict) -> dict:
        if 'criado_em' in data and isinstance(data['criado_em'], datetime):
            data['criado_em'] = formatar_data(data['criado_em'])
        if 'atualizado_em' in data and isinstance(
            data['atualizado_em'], datetime
        ):
            data['atualizado_em'] = formatar_data(data['atualizado_em'])
        return data


class CampoAdicionalResponse(BaseModel):
    id: uuid.UUID
    fk_campanha_id: uuid.UUID
    nome_campo: str
    tipo_campo: str
    obrigatorio: bool
    criado_em: str
    atualizado_em: Optional[str]

    @model_validator(mode='before')
    @classmethod
    def formatar_datas(cls, data: dict) -> dict:
        if 'criado_em' in data and isinstance(data['criado_em'], datetime):
            data['criado_em'] = formatar_data(data['criado_em'])
        if 'atualizado_em' in data and isinstance(
            data['atualizado_em'], datetime
        ):
            data['atualizado_em'] = formatar_data(data['atualizado_em'])
        return data


class LandingPageResponse(BaseModel):
    id: uuid.UUID
    fk_campanha_id: uuid.UUID
    conteudo: str
    shlink: Optional[str]
    criado_em: str
    atualizado_em: Optional[str]

    @model_validator(mode='before')
    @classmethod
    def formatar_datas(cls, data: dict) -> dict:
        if 'criado_em' in data and isinstance(data['criado_em'], datetime):
            data['criado_em'] = formatar_data(data['criado_em'])
        if 'atualizado_em' in data and isinstance(
            data['atualizado_em'], datetime
        ):
            data['atualizado_em'] = formatar_data(data['atualizado_em'])
        return data


class CampanhaCompletaResponse(BaseModel):
    campanha: CampanhaResponse
    landing_page: Optional[LandingPageResponse]


class ListagemCompletaDeCampanhaResponse(BaseModel):
    campanhas: List[CampanhaCompletaResponse]
    pagina: int
    total: int
    paginas: int
    por_pagina: int


class ListaCampanhaPorIdResponse(BaseModel):
    campanha: CampanhaCompletaResponse


class CampoAdicionalSemDataResponse(BaseModel):
    id: uuid.UUID
    fk_campanha_id: uuid.UUID
    nome_campo: str
    tipo_campo: str
    obrigatorio: bool


class ListaCampanhaPorNomeResponse(BaseModel):
    id: uuid.UUID
    nome: str
    objetivo: ObjetivosCampanhaEnum
    publica: bool
    fk_cargo_oficial_id: uuid.UUID | None
    campos_adicionais: List[CampoAdicionalSemDataResponse] | None


class ListaDeCampanhasSchema(BaseModel):
    id: uuid.UUID
    nome_campanha: str


class ListaDeCampanhasResponse(RootModel):
    root: list[ListaDeCampanhasSchema]
