from acutis_api.communication.requests.agape import (
    RegistrarDoacaoAgapeRequestSchema,
)
from acutis_api.communication.responses.agape import (
    ItemDoacaoDetalheResponseSchema,
    RegistrarDoacaoAgapeResponse,
)
from acutis_api.domain.entities.doacao_agape import DoacaoAgape
from acutis_api.domain.entities.instancia_acao_agape import StatusAcaoAgapeEnum
from acutis_api.domain.entities.item_doacao_agape import ItemDoacaoAgape
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
        familia = self.agape_repository.buscar_familia_por_id(
            request_data.familia_id
        )
        if not familia:
            raise HttpNotFoundError(
                f"""
                Família com ID {request_data.familia_id} não encontrada.
                """
            )

        ciclo_acao = self.agape_repository.buscar_ciclo_acao_agape_por_id(
            request_data.ciclo_acao_id
        )
        if not ciclo_acao:
            raise HttpNotFoundError(
                f"""
                Ciclo de ação com ID {request_data.ciclo_acao_id}
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

        itens_instancia_para_atualizar = []
        itens_doacao_criados_entidades = []

        for item_input in request_data.itens:
            item_instancia = (
                self.agape_repository.buscar_item_instancia_agape_por_id(
                    item_input.item_instancia_id
                )
            )
            if not item_instancia:
                raise HttpNotFoundError(
                    f"""
                    Item de instância de ação com ID
                    {item_input.item_instancia_id} não encontrado.
                    """
                )

            if item_instancia.fk_instancia_acao_agape_id != ciclo_acao.id:
                raise HttpUnprocessableEntityError(
                    f"""Item de instância com ID {item_instancia.id}
                    não pertence ao ciclo de ação com ID {ciclo_acao.id}.
                    """
                )

            if item_input.quantidade <= 0:
                raise HttpUnprocessableEntityError(
                    f"""Quantidade para o item {item_instancia.id}
                    deve ser maior que zero.
                    """
                )

            if item_input.quantidade > item_instancia.quantidade:
                raise HttpUnprocessableEntityError(
                    f'Quantidade solicitada ({item_input.quantidade}) \
                    para o item de instância {item_instancia.id} excede a \
                    quantidade disponível ({item_instancia.quantidade}).'
                )

            itens_instancia_para_atualizar.append((
                item_instancia,
                item_input.quantidade,
            ))

        nova_doacao_agape = DoacaoAgape(
            fk_familia_agape_id=familia.id,
            fk_instancia_acao_agape_id=ciclo_acao.id,
        )
        doacao_registrada = self.agape_repository.registrar_doacao_agape(
            nova_doacao_agape
        )

        for item_instancia, quantidade_doada in itens_instancia_para_atualizar:
            novo_item_doacao = ItemDoacaoAgape(
                fk_doacao_agape_id=doacao_registrada.id,
                fk_item_instancia_agape_id=item_instancia.id,
                quantidade=quantidade_doada,
            )
            item_doacao_criado = (
                self.agape_repository.registrar_item_doacao_agape(
                    novo_item_doacao
                )
            )
            itens_doacao_criados_entidades.append(item_doacao_criado)

            item_instancia.quantidade -= quantidade_doada
            self.agape_repository.atualizar_item_instancia_agape(
                item_instancia
            )

        self.agape_repository.salvar_alteracoes()

        itens_doados_response = [
            ItemDoacaoDetalheResponseSchema.model_validate(idc)
            for idc in itens_doacao_criados_entidades
        ]

        return RegistrarDoacaoAgapeResponse(
            id=doacao_registrada.id,
            familia_agape_id=doacao_registrada.fk_familia_agape_id,
            instancia_acao_agape_id=ciclo_acao.id,
            itens_doados=itens_doados_response,
            criado_em=doacao_registrada.criado_em,
        )
