from acutis_api.communication.responses.membros import (
    CardDoacoesMembroBenfeitorResponse,
    TotalPagoDoacoesSchema,
    UltimaDoacaoPagaSchema,
)
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.repositories.membros import MembrosRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscarCardDoacoesMembroBenfeitorUseCase:
    def __init__(self, repository: MembrosRepositoryInterface):
        self._repository = repository

    def execute(self, usuario_logado: Lead):
        if (
            not usuario_logado.membro
            or not usuario_logado.membro.fk_benfeitor_id
        ):
            raise HttpNotFoundError('Nenhuma doação encontrada.')

        card_doacoes = self._repository.buscar_card_doacoes_membro_benfeitor(
            usuario_logado.membro.fk_benfeitor_id
        )

        response = CardDoacoesMembroBenfeitorResponse(
            total_pago_doacoes=TotalPagoDoacoesSchema(
                valor_doado=card_doacoes.valor_doado,
                quantidade_doacoes=card_doacoes.quantidade_doacoes,
            ),
            ultima_doacao_paga=UltimaDoacaoPagaSchema(
                ultima_doacao=card_doacoes.ultima_doacao
            ),
        )

        return response
