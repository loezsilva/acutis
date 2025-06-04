from uuid import UUID
from http import HTTPStatus

from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.communication.responses.agape import (
    ListarDoacoesRecebidasFamiliaResponse, 
    DoacaoRecebidaItemDetalheSchema,
    DoacaoRecebidaDetalheSchema,
)
from acutis_api.exception.errors.not_found import HttpNotFoundError

class ListarDoacoesRecebidasFamiliaUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self._agape_repository = agape_repository

    def execute(
        self, familia_id: UUID
    ) -> tuple[ListarDoacoesRecebidasFamiliaResponse, HTTPStatus]:
        
        familia = self._agape_repository.buscar_familia_por_id(
            familia_id=familia_id
        )

        if familia is None:
            raise HttpNotFoundError(
                'Família não encontrada'
            )
        
        doacoes = (
            self._agape_repository.listar_doacoes_recebidas_por_familia(
                familia_id=familia_id
            )
        )

        doacoes_recebidas_data = []

        for doacao in doacoes:
            itens_doacao = self._agape_repository.listar_itens_por_doacao_agape_id(
                doacao_id=doacao.id
            )
            itens_data = []
            for item in itens_doacao:
                itens_data.append(
                    DoacaoRecebidaItemDetalheSchema(
                        nome_item=item.nome_item,
                        quantidade=item.quantidade_doada,
                    )
                )

            doacoes_recebidas_data.append(
                DoacaoRecebidaDetalheSchema(
                    id=doacao.id,
                    data_doacao=doacao.criado_em,
                    itens=itens_data,
                )
            )

        
        response_schema = ListarDoacoesRecebidasFamiliaResponse(
            root=doacoes_recebidas_data
        )

        return response_schema, HTTPStatus.OK