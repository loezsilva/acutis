from acutis_api.communication.requests.agape import (
    RegistrarItemEstoqueAgapeRequest,
)
from acutis_api.communication.responses.agape import (
    RegistrarItemEstoqueAgapeResponse,
)
from acutis_api.domain.repositories.agape import (
    AgapeRepositoryInterface,
)
from acutis_api.exception.errors.conflict import HttpConflictError


class RegistrarEstoqueAgapeUseCase:
    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__agape_repository = agape_repository

    def execute(
        self, dados: RegistrarItemEstoqueAgapeRequest
    ) -> RegistrarItemEstoqueAgapeResponse:
        verifica_item_estoque_ja_cadastrado = (
            self.__agape_repository.verificar_item_estoque(dados.item)
        )

        if verifica_item_estoque_ja_cadastrado is not None:
            raise HttpConflictError('Item já cadastrado')

        item = self.__agape_repository.registrar_item_estoque(dados=dados)

        self.__agape_repository.salvar_alteracoes()

        return RegistrarItemEstoqueAgapeResponse(
            id=item.id,
            item=item.item,
        ).model_dump()
