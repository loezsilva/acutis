from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ExcluirItemEstoqueAgapeUseCase:
    """
    Caso de uso para excluir um item do estoque Ágape completamente.
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self,
        item_id,
    ) -> None:
        # Busca o item de estoque pelo ID
        item = self.__repository.buscar_item_estoque_por_id(item_id)
        if item is None:
            raise HttpNotFoundError('Item não encontrado.')
        # Remove o item do banco
        self.__repository.remover_item_estoque(item)
        self.__repository.salvar_alteracoes()
