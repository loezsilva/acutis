import uuid

from acutis_api.communication.responses.agape import (
    ItemDoadoBeneficiarioResponse,
    ListarItensDoadosBeneficiarioResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarItensDoadosBeneficiarioUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, doacao_id: uuid.UUID
    ) -> ListarItensDoadosBeneficiarioResponse:
        doacao_agape = self.agape_repository.buscar_doacao_agape_por_id(
            doacao_id
        )
        if doacao_agape is None:
            raise HttpNotFoundError('Doação não encontrada.')

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
                        ),
                    )
                )

        return ListarItensDoadosBeneficiarioResponse(
            root=resultados_response
        ).model_dump()
