from acutis_api.communication.requests.vocacional import (
    ListarPreCadastrosQuery,
)
from acutis_api.communication.responses.vocacional import (
    ListarPreCadastrosResponse,
)
from acutis_api.domain.repositories.vocacional import (
    InterfaceVocacionalRepository,
)
from acutis_api.domain.services.file_service import FileServiceInterface

from .monta_vocacional import (
    MontaVocacionalUseCase,
)


class ListarPreCadastrosUseCase:
    def __init__(
        self,
        vocacional_repository: InterfaceVocacionalRepository,
        file_service: FileServiceInterface,
    ):
        self.__vocacional_repository = vocacional_repository
        self.__s3_client = file_service

    def execute(self, filtros: ListarPreCadastrosQuery):
        paginacao = self.__vocacional_repository.busca_pre_cadastro_vocacional(
            filtros
        )

        lista_pre_cadastros = []

        lista_pre_cadastros = MontaVocacionalUseCase(
            paginacao,
            self.__vocacional_repository,
            self.__s3_client,
        ).execute()

        response = {
            'pre_cadastros': lista_pre_cadastros,
            'pagina': paginacao.page,
            'total': paginacao.total,
        }
        return ListarPreCadastrosResponse.model_validate(response)
