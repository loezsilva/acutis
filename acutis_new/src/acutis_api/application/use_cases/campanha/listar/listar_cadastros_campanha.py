import uuid

from acutis_api.communication.responses.campanha import (
    ListarCadastrosCampanhaResponse,
    ListarCadastrosCampanhaSchema,
)
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.domain.repositories.schemas.paginacao import PaginacaoQuery


class ListarCadastrosCampanhaUseCase:
    def __init__(self, repository: CampanhaRepositoryInterface):
        self._repository = repository

    def execute(self, filtros: PaginacaoQuery, campanha_id: uuid.UUID):
        paginacao = self._repository.listar_cadastros_campanha_pelo_id(
            filtros, campanha_id
        )

        response = ListarCadastrosCampanhaResponse(
            pagina=paginacao.page,
            paginas=paginacao.pages,
            total=paginacao.total,
            cadastros=[
                ListarCadastrosCampanhaSchema.model_validate(cadastro)
                for cadastro in paginacao.items
            ],
        ).model_dump()
        return response
