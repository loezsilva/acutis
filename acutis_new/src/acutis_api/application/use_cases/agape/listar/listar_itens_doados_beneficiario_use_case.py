import uuid

from acutis_api.communication.responses.agape import (
    ItemDoadoBeneficiarioResponse,
    ListarItensDoadosBeneficiarioResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarItensDoadosBeneficiarioUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, doacao_id: uuid.UUID
    ) -> ListarItensDoadosBeneficiarioResponse:
        doacao_agape = self.agape_repository.buscar_doacao_agape_por_id(
            doacao_id
        )
        if doacao_agape is None:
            raise HttpNotFoundError('Doação não encontrada.')

        itens_doados_data = (
            self.agape_repository.listar_itens_por_doacao_agape_id(
                doacao_id=doacao_id
            )
        )

        resultados_respostas = []
        for item_data in itens_doados_data:
            resultados_respostas.append(
                ItemDoadoBeneficiarioResponse(
                    nome_item=item_data.nome_item,
                    quantidade=item_data.quantidade_doada,
                )
            )

        return ListarItensDoadosBeneficiarioResponse(
            resultados=resultados_respostas
        ).model_dump()
