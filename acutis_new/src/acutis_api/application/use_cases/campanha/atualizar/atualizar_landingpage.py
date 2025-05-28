from acutis_api.communication.requests.campanha import AtualizarLandpageRequest
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class AtualizarLandPageCampanhaUseCase:
    def __init__(self, repository: CampanhaRepositoryInterface):
        self.__repository = repository

    def execute(self, requisicao: AtualizarLandpageRequest):
        busca_landing_page = self.__repository.buscar_landing_page_por_id(
            requisicao.fk_landingpage_id
        )

        if busca_landing_page is None:
            raise HttpNotFoundError('Landing page não encontrada')

        self.__repository.atualizar_landing_page(
            landing_page=busca_landing_page,
            dados_da_landing_page=requisicao,
        )

        self.__repository.salvar_alteracoes()
