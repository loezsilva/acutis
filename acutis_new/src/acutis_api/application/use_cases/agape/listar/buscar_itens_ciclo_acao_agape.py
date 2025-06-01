from acutis_api.communication.responses.agape import (
    BuscarItensCicloAcaoAgapeResponse,
    DoacaoAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscarItensCicloAcaoAgapeUseCase:
    """
    Busca itens de um ciclo de ação Ágape pelo ID da instância.
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._repository = agape_repository

    def execute(
        self, acao_agape_id
    ) -> list[BuscarItensCicloAcaoAgapeResponse]:
        ciclo_acao = self._repository.buscar_ciclo_acao_agape_por_id(
            acao_agape_id
        )
        if ciclo_acao is None:
            raise HttpNotFoundError(
                f'Ciclo de ação Ágape com ID {acao_agape_id} não encontrado.'
            )

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
