from acutis_api.communication.responses.agape import (
    BuscarItensCicloAcaoAgapeResponse,
    DoacaoAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class BuscarItensCicloAcaoAgapeUseCase:
    """
    Busca itens de um ciclo de ação Ágape pelo ID da instância.
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._repository = agape_repository

    def execute(
        self, acao_agape_id
    ) -> list[BuscarItensCicloAcaoAgapeResponse]:
        itens = self._repository.buscar_itens_ciclo_acao_agape(acao_agape_id)

        response = BuscarItensCicloAcaoAgapeResponse(
            resultados=[
                DoacaoAgapeResponse(
                    id=item.id,
                    item_id=item.item_id,
                    item=item.item,
                    quantidade=item.quantidade,
                ).model_dump()
                for item in itens
            ],
        ).model_dump()

        return response
