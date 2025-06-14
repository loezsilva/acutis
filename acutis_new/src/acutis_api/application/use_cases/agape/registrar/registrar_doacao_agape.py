from acutis_api.communication.requests.agape import (
    RegistrarDoacaoAgapeRequestSchema,
)
from acutis_api.communication.responses.agape import (
    RegistrarDoacaoAgapeResponse,
)
from acutis_api.domain.entities.instancia_acao_agape import StatusAcaoAgapeEnum
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError
from acutis_api.exception.errors.unprocessable_entity import (
    HttpUnprocessableEntityError,
)


class RegistrarDoacaoAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, request_data: RegistrarDoacaoAgapeRequestSchema
    ) -> RegistrarDoacaoAgapeResponse:
        self.__valida_dados_da_familia(familia_id=request_data.familia_id)
        self.__valida_dados_da_ciclo_acao(ciclo_id=request_data.ciclo_acao_id)

        doacao_registrada = self.agape_repository.registrar_doacao_agape(
            request_data.familia_id
        )

        for doacao in request_data.doacoes:
            item_instancia_agape = (
                self.agape_repository.buscar_item_instancia_agape_por_id(
                    doacao.item_instancia_id
                )
            )

            if item_instancia_agape is None:
                raise HttpNotFoundError(
                    f'Item {doacao.item_instancia_id} não encontrado.'
                )

            if doacao.quantidade > item_instancia_agape.quantidade:
                raise HttpUnprocessableEntityError(
                    'O ciclo da ação possui itens com quantidades insuficientes para realizar esta doação.'  # noqa
                )

            self.agape_repository.registrar_item_doacao_agape(
                item_instancia_id=item_instancia_agape.id,
                doacao_id=doacao_registrada.id,
                quantidade=doacao.quantidade,
            )

            item_instancia_agape.quantidade -= doacao.quantidade

        self.agape_repository.salvar_alteracoes()

        return RegistrarDoacaoAgapeResponse(
            msg='Doação registrada com sucesso.',
            doacao_id=doacao_registrada.id,
        ).model_dump()

    def __valida_dados_da_familia(self, familia_id) -> None:
        familia = self.agape_repository.buscar_familia_por_id(familia_id)

        if familia is None or familia.deletado_em is not None:
            raise HttpNotFoundError('Família não encontrada.')

        if familia.status == False:
            raise HttpUnprocessableEntityError(
                'Familia com status inativo para receber doações.'
            )

    def __valida_dados_da_ciclo_acao(self, ciclo_id) -> None:
        ciclo_acao = self.agape_repository.buscar_ciclo_acao_agape_por_id(
            ciclo_id
        )
        if not ciclo_acao:
            raise HttpNotFoundError(
                f"""
                Ciclo de ação com ID {ciclo_id}
                não encontrado.
                """
            )

        if ciclo_acao.status != StatusAcaoAgapeEnum.em_andamento:
            raise HttpUnprocessableEntityError(
                f"""
                Doações só podem ser registradas em ciclos de ação
                'em_andamento'. Status atual: {ciclo_acao.status.value}.
                """
            )
