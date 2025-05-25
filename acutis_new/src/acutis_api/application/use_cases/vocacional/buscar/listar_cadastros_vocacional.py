from acutis_api.communication.requests.vocacional import (
    ListarCadastrosVocacionaisQuery,
)
from acutis_api.communication.responses.vocacional import (
    ListarCadastrosVocacionaisResponse,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.domain.services.file_service import FileServiceInterface

from .monta_vocacional import (
    MontaVocacionalUseCase,
)


class ListarCadastrosVocacionaisUseCase:
    def __init__(
        self,
        vocacional_repository: InterfaceVocacionalRepository,
        file_service: FileServiceInterface,
    ):
        self.__vocacional_repository = vocacional_repository
        self.__s3_client = file_service

    def execute(self, filtros: ListarCadastrosVocacionaisQuery):
        paginacao = self.__vocacional_repository.buscar_cadastros_vocacional(
            filtros
        )
        lista_cadastros_vocacionais = []

        lista_cadastros_vocacionais = MontaVocacionalUseCase(
            paginacao,
            self.__vocacional_repository,
            self.__s3_client,
        ).execute()

        response = {
            'cadastros_vocacionais': lista_cadastros_vocacionais,
            'pagina': paginacao.page,
            'total': paginacao.total,
        }
        return ListarCadastrosVocacionaisResponse.model_validate(response)
