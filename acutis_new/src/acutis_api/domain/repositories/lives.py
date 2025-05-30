from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import Optional
from uuid import UUID

from acutis_api.communication.requests.lives import (
    ObterHistogramaLiveRequest,
    ObterTodasLivesAvulsasRequest,
    ObterTodasLivesRecorrentesRequest,
)
from acutis_api.communication.responses.lives import (
    ObterTodasLivesAvulsasResponse,
    ObterTodasLivesRecorrentesResponse,
)
from acutis_api.domain.entities.audiencia_live import AudienciaLive
from acutis_api.domain.entities.live import Live
from acutis_api.domain.entities.live_avulsa import LiveAvulsa
from acutis_api.domain.entities.live_recorrente import LiveRecorrente


class LivesRepositoryInterface(ABC):
    @abstractmethod
    def salvar_dados(self): ...

    @abstractmethod
    def criar_canal(
        self, tag: str, rede_social: str, fk_campanha_id: UUID | None
    ): ...

    @abstractmethod
    def checar_existencia_canal(self, tag: str, rede_social: str) -> bool: ...

    @abstractmethod
    def obter_canal(self, tag: str, rede_social: str): ...

    @abstractmethod
    def registrar_live_avulsa(self, dados_live_avulsa): ...

    @abstractmethod
    def registrar_live_recorrente(self, dados_live_recorrente): ...

    @abstractmethod
    def obter_lives_programadas(self): ...

    @abstractmethod
    def editar_programacao_live(
        self, programacao_id: UUID, tipo_programacao: str, **kwargs
    ): ...

    def buscar_programacao_por_id(
        self, programacao_id: UUID, model: LiveAvulsa | LiveRecorrente
    ): ...

    @abstractmethod
    def deletar_programacao_live(
        self, programacao_id: int, tipo_programacao: str
    ) -> bool: ...

    def obter_live_por_id(self, live_id: UUID) -> Live | None: ...

    @abstractmethod
    def obter_todas_lives_recorrentes(
        self, filtros: ObterTodasLivesRecorrentesRequest
    ) -> ObterTodasLivesRecorrentesResponse: ...

    @abstractmethod
    def obter_todas_lives_avulsas(
        self, filtros: ObterTodasLivesAvulsasRequest
    ) -> ObterTodasLivesAvulsasResponse: ...

    @abstractmethod
    def obter_audiencia_lives(
        self,
        live_id: UUID,
        initial_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> list[AudienciaLive]: ...

    @abstractmethod
    def obter_datas_lives_ocorridas(self) -> list[date]: ...

    @abstractmethod
    def obter_dados_histograma(
        self, request: ObterHistogramaLiveRequest
    ) -> dict: ...
