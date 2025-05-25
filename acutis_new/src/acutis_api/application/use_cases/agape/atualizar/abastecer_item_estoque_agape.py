from acutis_api.communication.responses.agape import ItemEstoqueAgapeResponse
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class AbastecerItemEstoqueAgapeUseCase:
    """
    Caso de uso para abastecer (incrementar)
    a quantidade de um item no estoque Ágape.
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self,
        item_id,
        quantidade: int,
    ) -> dict:
        # Busca o item de estoque pelo ID
        item = self.__repository.buscar_item_estoque_por_id(item_id)
        item_quantidade = int(item.quantidade)

        # Incrementa a quantidade
        item.quantidade = item_quantidade + quantidade

        # Persiste as alterações
        self.__repository.salvar_alteracoes()

        # Prepara a resposta
        response = ItemEstoqueAgapeResponse.model_validate(item).model_dump()

        return response
