from uuid import UUID

from acutis_api.communication.responses.agape import (
    DoacaoAgapeResponse,
    EnderecoResponse,
    UltimoCicloAcaoAgapeResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscarUltimaAcaoAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._agape_repository = agape_repository

    def execute(self, nome_acao_id: UUID) -> UltimoCicloAcaoAgapeResponse:
        nome_acao = self._agape_repository.buscar_nome_acao_por_id(
            nome_acao_id
        )
        if nome_acao is None:
            raise HttpNotFoundError(
                f'Nome da ação com ID {nome_acao_id} não encontrado.'
            )

        ultimo_ciclo_acao = (
            self._agape_repository.buscar_ultimo_ciclo_acao_por_nome_acao_id(
                nome_acao_id
            )
        )
        if ultimo_ciclo_acao is None:
            raise HttpNotFoundError(
                f"""Nenhum ciclo de ação encontrado para o
                nome da ação com ID {nome_acao_id}."""
            )

        endereco_response_data = None
        if ultimo_ciclo_acao.fk_endereco_id:
            endereco = self._agape_repository.buscar_endereco_por_id(
                ultimo_ciclo_acao.fk_endereco_id
            )
            if endereco:
                endereco_response_data = EnderecoResponse.model_validate(
                    endereco
                )

        itens_do_ciclo_schemas = (
            self._agape_repository.buscar_doacoes_ciclo_acao_agape(
                ultimo_ciclo_acao.id
            )
        )

        itens_do_ciclo_responses = [
            DoacaoAgapeResponse.model_validate(item_schema)
            for item_schema in itens_do_ciclo_schemas
        ]

        return UltimoCicloAcaoAgapeResponse(
            id=ultimo_ciclo_acao.id,
            abrangencia=ultimo_ciclo_acao.abrangencia,
            status=ultimo_ciclo_acao.status,
            data_inicio=ultimo_ciclo_acao.data_inicio,
            data_termino=ultimo_ciclo_acao.data_termino,
            endereco=endereco_response_data,
            itens_do_ciclo=itens_do_ciclo_responses,
            criado_em=ultimo_ciclo_acao.criado_em,
            atualizado_em=ultimo_ciclo_acao.atualizado_em,
        )
