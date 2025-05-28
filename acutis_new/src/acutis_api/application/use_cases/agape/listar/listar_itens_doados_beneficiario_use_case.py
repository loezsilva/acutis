import uuid
from http import HTTPStatus

from acutis_api.domain.repositories.agape import (
    AgapeRepositoryInterface
)
from acutis_api.communication.responses.agape import (
    ListarItensDoadosBeneficiarioResponse,
    ItemDoadoBeneficiarioResponse,
)

class ListarItensDoadosBeneficiarioUseCase:
    """
    Caso de uso para listar os itens doados para um beneficiário (via ID da DoacaoAgape).
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, doacao_id: uuid.UUID
    ) -> tuple[ListarItensDoadosBeneficiarioResponse, HTTPStatus]:
        
        itens_doados_data = (
            self.agape_repository.listar_itens_por_doacao_agape_id(
                doacao_id=doacao_id
            )
        )

        resultados_response = []
        if itens_doados_data:
            for item_data in itens_doados_data:
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
                        )
                    )
                )
        
        return ListarItensDoadosBeneficiarioResponse(
            root=resultados_response
        ), HTTPStatus.OK
