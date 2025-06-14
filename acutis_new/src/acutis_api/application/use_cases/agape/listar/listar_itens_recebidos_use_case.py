import uuid

from acutis_api.communication.responses.agape import (
    ItemDoadoBeneficiarioResponse,
    ListarItensDoadosBeneficiarioResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarItensRecebidosUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, ciclo_acao_id: uuid.UUID, doacao_id: uuid.UUID
    ) -> ListarItensDoadosBeneficiarioResponse:
        ciclo_acao = self.agape_repository.buscar_ciclo_acao_agape_por_id(
            ciclo_acao_id
        )

        if ciclo_acao is None:
            raise HttpNotFoundError('Ciclo ação não encontrado.')

        doacao = self.agape_repository.buscar_doacao_agape_por_id(doacao_id)
        if doacao is None:
            raise HttpNotFoundError('Doação não encontrada.')

        itens_recebidos = (
            self.agape_repository.listar_itens_recebidos_por_ciclo_e_doacao_id(
                ciclo_acao_id=ciclo_acao_id, doacao_id=doacao_id
            )
        )

        resultados_respostas = []
        for item_data in itens_recebidos:
            resultados_respostas.append(
                ItemDoadoBeneficiarioResponse.model_validate(
                    dict(item_data._mapping)
                )
            )

        return ListarItensDoadosBeneficiarioResponse(
            resultados=resultados_respostas
        ).model_dump()
