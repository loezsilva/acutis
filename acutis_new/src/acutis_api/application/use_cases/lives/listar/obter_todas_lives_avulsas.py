from acutis_api.communication.requests.lives import (
    ObterTodasLivesAvulsasRequest,
)
from acutis_api.communication.responses.lives import (
    LiveAvulsaResponseItem,
    ObterTodasLivesAvulsasResponse,
)
from acutis_api.domain.repositories.lives import LivesRepositoryInterface


class ObterTodasLivesAvulsasUseCase:
    def __init__(self, repository: LivesRepositoryInterface):
        self.repository = repository

    def execute(
        self, filtros: ObterTodasLivesAvulsasRequest
    ) -> ObterTodasLivesAvulsasResponse:
        paginacao = self.repository.obter_todas_lives_avulsas(filtros)

        responses = []
        for live_rec in paginacao.items:
            live = self.repository.obter_live_por_id(live_rec.fk_live_id)
            if live:
                responses.append(
                    LiveAvulsaResponseItem(
                        tag=live.tag,
                        rede_social=live.rede_social,
                        data_hora_inicio=live_rec.data_hora_inicio,
                    )
                )

        response = ObterTodasLivesAvulsasResponse(
            pagina=paginacao.page,
            por_pagina=paginacao.per_page,
            paginas=paginacao.pages,
            total=paginacao.total,
            agendamentos_avulsos=responses,
        )

        return response.model_dump()
