import uuid
from typing import List

from acutis_api.communication.requests.agape import (
    RegistrarRecibosRequestSchema,
)
from acutis_api.communication.responses.agape import (
    ReciboAgapeResponse,
    RegistrarRecibosResponse,
)
from acutis_api.domain.entities.recibo_agape import ReciboAgape
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class RegistrarRecibosDoacaoAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, doacao_id: uuid.UUID, request_data: RegistrarRecibosRequestSchema
    ) -> RegistrarRecibosResponse:
        doacao = self.agape_repository.buscar_doacao_agape_por_id(doacao_id)

        if not doacao:
            raise HttpNotFoundError(
                f'Doação com ID {doacao_id} não encontrada.'
            )

        recibos_criados_entidades: List[ReciboAgape] = []

        if not request_data.recibos:
            raise HttpBadRequestError('Você deve informar os recibos')

        for recibo_input in request_data.recibos:
            novo_recibo = ReciboAgape(
                fk_doacao_agape_id=doacao.id, recibo=recibo_input.recibo
            )
            recibo_persistido = self.agape_repository.registrar_recibo_agape(
                novo_recibo
            )
            recibos_criados_entidades.append(recibo_persistido)

        if recibos_criados_entidades:
            self.agape_repository.salvar_alteracoes()

        recibos_response_list = [
            ReciboAgapeResponse.model_validate(recibo_ent)
            for recibo_ent in recibos_criados_entidades
        ]

        return RegistrarRecibosResponse(
            recibos_criados=recibos_response_list
        ).model_dump()
