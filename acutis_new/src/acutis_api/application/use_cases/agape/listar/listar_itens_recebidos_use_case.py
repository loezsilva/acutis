import uuid
from http import HTTPStatus

from acutis_api.communication.responses.agape import (
    ItemDoadoBeneficiarioResponse,
    ListarItensDoadosBeneficiarioResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class ListarItensRecebidosUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, ciclo_acao_id: uuid.UUID, doacao_id: uuid.UUID
    ) -> tuple[ListarItensDoadosBeneficiarioResponse, HTTPStatus]:
        itens_recebidos_data = (
            self.agape_repository.listar_itens_recebidos_por_ciclo_e_doacao_id(
                ciclo_acao_id=ciclo_acao_id, doacao_id=doacao_id
            )
        )

        resultados_response = []
        if itens_recebidos_data:
            for item_data in itens_recebidos_data:
                resultados_response.append(
                    ItemDoadoBeneficiarioResponse(
                        item_id=getattr(item_data, 'item_id'),
                        nome_item=getattr(item_data, 'nome_item'),
                        quantidade_doada=getattr(
                            item_data, 'quantidade_doada'
                        ),
                        item_doacao_agape_id=getattr(
                            item_data, 'item_doacao_agape_id'
                        ),
                        item_instancia_agape_id=getattr(
                            item_data, 'item_instancia_agape_id'
                        ),
                    )
                )

        return ListarItensDoadosBeneficiarioResponse(
            root=resultados_response
        ), HTTPStatus.OK
