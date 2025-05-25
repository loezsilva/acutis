import uuid

from acutis_api.domain.entities import Lead
from acutis_api.domain.entities.pagamento_doacao import FormaPagamentoEnum
from acutis_api.domain.repositories.doacoes import DoacoesRepositoryInterface
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.forbidden import HttpForbiddenError
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.infrastructure.services.maxipago import MaxiPago


class CancelarRecorrenciaDoacaoUseCase:
    def __init__(
        self, repository: DoacoesRepositoryInterface, maxipago: MaxiPago
    ):
        self._repository = repository
        self._maxipago = maxipago

    def execute(self, doacao_id: uuid.UUID, lead: Lead):
        doacao = self._repository.buscar_doacao_por_id(doacao_id)
        if not doacao or not doacao.pagamento_doacao.recorrente:
            raise HttpNotFoundError(
                f'Ops, doação recorrente com id {doacao_id} não encontrada.'
            )

        if not doacao.pagamento_doacao.ativo:
            raise HttpConflictError(
                'Esta doação já se encontra com status cancelado.'
            )

        # TODO: Adicionar permissão de administrador
        if doacao.fk_benfeitor_id != lead.membro.fk_benfeitor_id:
            raise HttpForbiddenError(
                'Você não tem permissão para cancelar esta doação.'
            )

        match doacao.pagamento_doacao.forma_pagamento:
            case FormaPagamentoEnum.credito:
                self._maxipago.cancelar_pagamento_recorrente(
                    doacao.pagamento_doacao.codigo_ordem_pagamento
                )

        self._repository.cancelar_doacao_recorrente(doacao, lead)

        self._repository.salvar_alteracoes()
