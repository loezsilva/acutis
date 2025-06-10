import uuid
from datetime import datetime
from types import NoneType
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    RootModel,
    field_validator,
    model_validator,
)

from acutis_api.communication.enums.campanhas import (
    ObjetivosCampanhaEnum,
    PeriodicidadePainelCampanhasEnum,
)
from acutis_api.communication.responses.padrao import PaginacaoResponse


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
    fk_cargo_oficial_id: Optional[uuid.UUID]

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
    nome_campo: str
    tipo_campo: str
    obrigatorio: bool


class LandingPageResponse(BaseModel):
    id: uuid.UUID


class CampanhaCompletaResponse(BaseModel):
    campanha: CampanhaResponse
    landing_page: Optional[LandingPageResponse]
    campos_adicionais: Optional[List[CampoAdicionalResponse]]


class ListagemCompletaDeCampanhaResponse(BaseModel):
    campanhas: List[CampanhaCompletaResponse]
    pagina: int
    total: int
    paginas: int
    por_pagina: int


class ListaCampanhaPorIdResponse(RootModel):
    root: CampanhaCompletaResponse


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
    landingpage_id: Optional[uuid.UUID]


class ListaDeCampanhasSchema(BaseModel):
    id: uuid.UUID
    nome_campanha: str


class ListaDeCampanhasResponse(RootModel):
    root: list[ListaDeCampanhasSchema]


class PainelCampanhasSchema(BaseModel):
    nome_campanha: str
    objetivo: ObjetivosCampanhaEnum
    total: float
    periodicidade: PeriodicidadePainelCampanhasEnum
    porcentagem_crescimento: float


class PainelCampanhasResponse(BaseModel):
    campanhas: List[PainelCampanhasSchema]


class ListarDoacoesCampanhaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    valor: float
    data_doacao: datetime | str | None
    forma_pagamento: str
    nome: str

    @field_validator('data_doacao')
    @classmethod
    def formatar_datetime(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y - %H:%M:%S')


class ListarDoacoesCampanhaResponse(PaginacaoResponse):
    doacoes: list[ListarDoacoesCampanhaSchema]


class ListarCadastrosCampanhaSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    email: str
    telefone: str
    data_cadastro: datetime | str | None

    @field_validator('data_cadastro')
    @classmethod
    def formatar_datetime(cls, value: datetime):
        if isinstance(value, (str, NoneType)):
            return value

        return value.strftime('%d/%m/%Y - %H:%M:%S')


class ListarCadastrosCampanhaResponse(PaginacaoResponse):
    cadastros: list[ListarCadastrosCampanhaSchema]


class CadastrosCampanhaPorPeriodoResponse(BaseModel):
    ultimas_24h: int
    ultimos_7_dias: int
    ultimo_mes: int
