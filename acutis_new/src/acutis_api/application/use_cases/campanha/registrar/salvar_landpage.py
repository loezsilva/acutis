from acutis_api.communication.requests.campanha import SalvarLandpageRequest
from acutis_api.communication.responses.padrao import ResponsePadraoSchema
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.exception.errors.conflict import HttpConflictError
from acutis_api.exception.errors.not_found import HttpNotFoundError


class SalvarLandPageCampanhaUseCase:
    def __init__(self, repository: CampanhaRepositoryInterface):
        self.__repository = repository

    def execute(
        self, requisicao: SalvarLandpageRequest
    ) -> ResponsePadraoSchema:
        if requisicao.conteudo is None:
            raise HttpBadRequestError('Conteudo não pode ser nulo')

        busca_campanha = self.__repository.buscar_campanha_por_nome(
            requisicao.nome_campanha
        )

        if busca_campanha is None:
            raise HttpNotFoundError('Campanha não encontrada')

        campanha, landing_page = busca_campanha

        busca_landing_page = (
            self.__repository.buscar_landing_page_por_campanha_id(campanha.id)
        )

        if busca_landing_page is not None:
            raise HttpConflictError('Essa campanha já possui uma landing page')

        self.__repository.criar_landing_page(
            fk_campanha_id=campanha.id, dados_da_landing_page=requisicao
        )

        self.__repository.salvar_alteracoes()
