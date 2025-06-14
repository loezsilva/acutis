from acutis_api.domain.entities.estoque_agape import EstoqueAgape
from acutis_api.domain.entities.instancia_acao_agape import (
    StatusAcaoAgapeEnum,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class DeletarCicloAcaoAgapeUseCase:
    """
    Deleta um ciclo de ação Ágape não iniciado, retornando itens ao estoque.
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.__repository = agape_repository

    def execute(self, acao_agape_id) -> None:
        ciclo_acao = self.__repository.buscar_ciclo_acao_agape_por_id(
            acao_agape_id
        )

        if ciclo_acao is None:
            raise HttpNotFoundError('Ciclo da ação não encontrado.')

        if ciclo_acao.status != StatusAcaoAgapeEnum.nao_iniciado:
            raise HttpBadRequestError(
                'Somentes ciclos não iniciados podem ser deletados.'
            )

        # Retorna itens ao estoque
        itens = self.__repository.listar_itens_ciclo_acao_agape(ciclo_acao.id)

        for item in itens:
            item_estoque: EstoqueAgape = (
                self.__repository.buscar_item_estoque_por_id(
                    item.fk_estoque_agape_id
                )
            )

            if item_estoque.quantidade > 0:
                item_estoque.quantidade += item.quantidade

            self.__repository.movimentar_historico_ciclo_acao_agape(
                item_id=item_estoque.id,
                quantidade=item.quantidade,
            )

            self.__repository.deletar_item_ciclo_acao_agape(item)

        self.__repository.deletar_ciclo_acao_agape(acao_agape_id)

        self.__repository.salvar_alteracoes()
