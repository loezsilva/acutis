from acutis_api.domain.entities.instancia_acao_agape import (
    StatusAcaoAgapeEnum,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class IniciarCicloAcaoAgapeUseCase:
    """
    Inicia o ciclo de uma ação Ágape, marcando status e data de início.
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
            raise HttpUnprocessableEntityError(
                'Ciclo da ação já iniciado ou finalizado.'
            )

        if self.__repository.verificar_ciclo_acao_iniciado(ciclo_acao):
            raise HttpConflictError(
                'Essa ação ágape já possui um ciclo em andamento.'
            )

        self.__repository.iniciar_ciclo_acao_agape(ciclo_acao)

        self.__repository.salvar_alteracoes()
