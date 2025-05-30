from acutis_api.communication.requests.lives import (
    ObterTodasLivesRecorrentesRequest,
)
from acutis_api.communication.responses.lives import (
    LiveRecorrenteResponse,
    ObterTodasLivesRecorrentesResponse,
)
from acutis_api.domain.repositories.lives import LivesRepositoryInterface


class ObterTodasLivesRecorrentesUseCase:
    def __init__(self, repository: LivesRepositoryInterface):
        self.repository = repository

    def execute(self, filtros: ObterTodasLivesRecorrentesRequest) -> dict:
        paginacao = self.repository.obter_todas_lives_recorrentes(filtros)

        DATA_RE = '%H:%M:%S'

        agendamentos = [
            LiveRecorrenteResponse(
                agendamento_rec_id=recorrente.id,
                dia_semana=recorrente.dia_semana,
                campanha_id=self.__busca_live(
                    recorrente.fk_live_id
                ).fk_campanha_id,
                rede_social=self.__busca_live(
                    recorrente.fk_live_id
                ).rede_social,
                tag=self.__busca_live(recorrente.fk_live_id).tag,
                live_id=recorrente.fk_live_id,
                hora_inicio=recorrente.hora_inicio.strftime(DATA_RE),
            )
            for recorrente in paginacao.items
        ]

        response = ObterTodasLivesRecorrentesResponse(
            pagina=paginacao.page,
            por_pagina=paginacao.per_page,
            paginas=paginacao.pages,
            total=paginacao.total,
            agendamentos_recorrentes=agendamentos,
        )

        return response.model_dump()

    def __busca_live(self, fk_live_id):
        return self.repository.obter_live_por_id(fk_live_id)
