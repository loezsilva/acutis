from acutis_api.application.utils.funcoes_auxiliares import normalizar_texto
from acutis_api.communication.requests.agape import (
    RegistrarItemEstoqueAgapeRequest,
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

    def execute(self, dados: RegistrarItemEstoqueAgapeRequest) -> None:
        nome_item = normalizar_texto(dados.item)

        verifica_item_estoque_ja_cadastrado = (
            self.__agape_repository.verificar_item_estoque(nome_item)
        )

        if verifica_item_estoque_ja_cadastrado is not None:
            raise HttpConflictError('Item já cadastrado')

        self.__agape_repository.registrar_item_estoque(
            item_nome=nome_item, quantidade=0
        )

        self.__agape_repository.salvar_alteracoes()
