from acutis_api.communication.requests.vocacional import (
    ListarFichasVocacionaisQuery,
)
from acutis_api.communication.responses.vocacional import (
    ListarFichasVocacionaisResponse,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.domain.services.file_service import FileServiceInterface

from .monta_vocacional import MontaVocacionalUseCase


class ListarFichasVocacionaisUseCase:
    def __init__(
        self,
        vocacional_repository: InterfaceVocacionalRepository,
        file_service: FileServiceInterface,
    ):
        self.__vocacional_repository = vocacional_repository
        self.__s3_client = file_service

    def execute(self, filtros: ListarFichasVocacionaisQuery):
        paginacao = self.__vocacional_repository.buscar_fichas_vocacionais(
            filtros
        )
        lista_fichas_vocacionais = []

        lista_fichas_vocacionais = MontaVocacionalUseCase(
            paginacao,
            self.__vocacional_repository,
            self.__s3_client,
        ).execute()
        response = {
            'fichas_vocacionais': lista_fichas_vocacionais,
            'pagina': paginacao.page,
            'total': paginacao.total,
        }
        return ListarFichasVocacionaisResponse.model_validate(response)
