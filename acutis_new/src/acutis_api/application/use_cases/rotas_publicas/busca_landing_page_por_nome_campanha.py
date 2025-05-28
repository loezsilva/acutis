from acutis_api.communication.responses.rotas_publicas import (
    BuscaLandingPageDaCampanhaResponse,
)
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class LandingpageDaCampanhaUseCase:
    def __init__(self, repository: CampanhaRepositoryInterface):
        self.__repository = repository

    def execute(self, nome_campanha: str):
        busca_lp = self.__repository.busca_lp_por_nome_campanha(nome_campanha)

        if busca_lp is None:
            raise HttpNotFoundError('Nome de campanha não encontrado')

        return BuscaLandingPageDaCampanhaResponse(
            conteudo=busca_lp.conteudo, estrutura_json=busca_lp.estrutura_json
        ).model_dump()
