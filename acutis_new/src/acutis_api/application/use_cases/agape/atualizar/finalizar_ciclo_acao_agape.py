from acutis_api.domain.entities.instancia_acao_agape import (
    StatusAcaoAgapeEnum,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class FinalizarCicloAcaoAgapeUseCase:
    """
    Finaliza o ciclo de uma ação Ágape, retornando itens restantes ao estoque.
    """

    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, acao_agape_id):
        ciclo_acao = self.__repository.buscar_ciclo_acao_agape_por_id(
            acao_agape_id
        )

        if ciclo_acao is None:
            raise HttpNotFoundError('Ciclo da ação não encontrado.')

        if self.__repository.verificar_ciclo_acao_finalizado(ciclo_acao):
            raise HttpConflictError(
                'Essa ação ágape já possui um ciclo em andamento.'
            )

        if ciclo_acao.status != StatusAcaoAgapeEnum.em_andamento:
            raise HttpUnprocessableEntityError(
                'Ciclo da ação ainda não foi iniciado ou já foi finalizado.'
            )

        # Retorna itens restantes
        itens = self.__repository.listar_itens_ciclo_acao_agape(ciclo_acao.id)

        for item in itens:
            item_estoque = self.__repository.buscar_item_estoque_por_id(
                item.fk_estoque_agape_id
            )

            if item_estoque.quantidade > 0:
                item_estoque.quantidade += item.quantidade

            self.__repository.movimentar_historico_ciclo_acao_agape(
                item_estoque.id,
                ciclo_acao.id,
                quantidade=item.quantidade,
            )

            item.quantidade = 0

        self.__repository.finalizar_ciclo_acao_agape(ciclo_acao)

        self.__repository.salvar_alteracoes()

        return {'msg': 'Ciclo da ação finalizado com sucesso.'}
