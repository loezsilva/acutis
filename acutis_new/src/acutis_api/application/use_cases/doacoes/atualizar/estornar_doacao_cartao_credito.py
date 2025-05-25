import uuid

from acutis_api.domain.entities import Lead
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.domain.repositories.doacoes import DoacoesRepositoryInterface
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.infrastructure.services.maxipago import MaxiPago


class EstornarDoacaoCartaoCreditoUseCase:
    def __init__(
        self, repository: DoacoesRepositoryInterface, maxipago: MaxiPago
    ):
        self._repository = repository
        self._maxipago = maxipago

    def execute(self, processamento_doacao_id: uuid.UUID, lead: Lead):
        # TODO: Adicionar permissão de estorno de doacao para administrador

        processamento_doacao = (
            self._repository.buscar_processamento_doacao_por_id(
                processamento_doacao_id
            )
        )
        if not processamento_doacao:
            raise HttpNotFoundError(
                f'Ops, processamento da doação com id {processamento_doacao_id} não encontrado.'  # noqa
            )

        if processamento_doacao.status == StatusProcessamentoEnum.estornado:
            raise HttpConflictError(
                'Ops, essa doação já consta como estornada.'
            )

        self._maxipago.estornar_pagamento(
            codigo_ordem_pagamento=(
                processamento_doacao.pagamento_doacao.codigo_ordem_pagamento
            ),
            codigo_referencia=processamento_doacao.codigo_referencia,
            valor=processamento_doacao.pagamento_doacao.valor,
        )

        if processamento_doacao.pagamento_doacao.recorrente:
            self._repository.estornar_processamento_doacao_recorrente(
                processamento_doacao
            )
        else:
            self._repository.estornar_processamento_doacao_unica(
                processamento_doacao
            )

        self._repository.salvar_alteracoes()
