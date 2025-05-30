import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, RootModel

from acutis_api.communication.responses.padrao import PaginacaoResponse


class ObterCanalSchema(BaseModel):
    id: uuid.UUID
    tag: str
    rede_social: str


class ListaObterCanalResponse(RootModel):
    root: list[ObterCanalSchema]


class ObterLivesProgramadasResponse(BaseModel):
    id: uuid.UUID
    tag: str
    rede_social: str
    tipo_programacao: str


class ListaObterLivesProgramadasResponse(RootModel):
    root: List[ObterLivesProgramadasResponse]


class LiveRecorrenteResponse(BaseModel):
    agendamento_rec_id: uuid.UUID
    dia_semana: str
    campanha_id: uuid.UUID
    rede_social: str
    tag: str
    live_id: uuid.UUID
    hora_inicio: str


class ObterTodasLivesRecorrentesResponse(PaginacaoResponse):
    agendamentos_recorrentes: List[LiveRecorrenteResponse]


class LiveAvulsaResponseItem(BaseModel):
    tag: Optional[str] = None
    rede_social: Optional[str] = None
    data_hora_inicio: Optional[datetime] = None


class ObterTodasLivesAvulsasResponse(PaginacaoResponse):
    agendamentos_avulsos: List[LiveAvulsaResponseItem]


class AudienciaLiveResponseItem(BaseModel):
    titulo: str
    data_hora: datetime
    audiencia: int


class ObterAudienciaLivesResponse(RootModel):
    root: list[AudienciaLiveResponseItem]


class ObterDatasLivesOcorridasResponse(BaseModel):
    datas: List[str]


class HistogramaLiveItem(BaseModel):
    horario: str
    audiencia: int


class LiveDataItem(BaseModel):
    titulo: str
    dados: List[HistogramaLiveItem]


class ObterHistogramaLiveResponse(BaseModel):
    audiencia_maxima: int
    audiencia_minima: int
    audiencia_media: int
    canal_principal: str
    live_data: List[LiveDataItem]
