from acutis_api.communication.responses.campanha import (
    CampoAdicionalSemDataResponse,
    ListaCampanhaPorNomeResponse,
)
from acutis_api.domain.repositories.campanha import CampanhaRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class BuscaCampanhaPorNomeUseCase:
    def __init__(self, membro_repository: CampanhaRepositoryInterface):
        self.__repository = membro_repository

    def execute(self, nome_campanha: str) -> ListaCampanhaPorNomeResponse:
        busca_campanha = self.__repository.buscar_campanha_por_nome(
            nome_campanha
        )

        if busca_campanha is None:
            raise HttpNotFoundError('Campanha não encontrada')

        campanha, landing_page = busca_campanha

        campos_adicionais = self.__repository.buscar_campos_adicionais(
            campanha.id
        )

        campos_adicionais_response = []
        if campos_adicionais is not None:
            for campo in campos_adicionais:
                campos_adicionais_response.append(
                    CampoAdicionalSemDataResponse(
                        id=campo.id,
                        fk_campanha_id=campo.fk_campanha_id,
                        nome_campo=campo.nome_campo,
                        tipo_campo=campo.tipo_campo,
                        obrigatorio=campo.obrigatorio,
                    )
                )

        campanha_response = ListaCampanhaPorNomeResponse(
            id=campanha.id,
            nome=campanha.nome,
            objetivo=campanha.objetivo,
            publica=campanha.publica,
            fk_cargo_oficial_id=campanha.fk_cargo_oficial_id,
            campos_adicionais=campos_adicionais_response,
            landingpage_id=landing_page.id if landing_page else None,
        ).model_dump()

        return campanha_response
