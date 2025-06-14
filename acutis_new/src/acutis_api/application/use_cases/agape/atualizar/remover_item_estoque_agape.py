from acutis_api.communication.requests.agape import (
    AbastecerItemEstoqueAgapeRequest,
)
from acutis_api.communication.responses.agape import ItemEstoqueAgapeResponse
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class RemoverItemEstoqueAgapeUseCase:
    """
    Caso de uso para remover (decrementar) a
    quantidade de um item no estoque Ágape.
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self,
        item_id,
        dados: AbastecerItemEstoqueAgapeRequest,
    ) -> ItemEstoqueAgapeResponse:
        # Busca o item de estoque pelo ID
        item = self.__repository.buscar_item_estoque_por_id(item_id)
        if item is None:
            raise HttpNotFoundError('Item não encontrado.')
        item_quantidade = int(item.quantidade)

        # Verifica se há estoque suficiente
        if dados.quantidade > item_quantidade:
            raise HttpBadRequestError(
                'Quantidade a remover maior que a quantidade em estoque'
            )

        # Decrementa a quantidade
        item.quantidade -= dados.quantidade

        # Persiste as alterações
        self.__repository.salvar_alteracoes()

        # Prepara a resposta
        response = ItemEstoqueAgapeResponse(
            id=item.id, item=item.item, quantidade=item.quantidade
        ).model_dump()

        return response
