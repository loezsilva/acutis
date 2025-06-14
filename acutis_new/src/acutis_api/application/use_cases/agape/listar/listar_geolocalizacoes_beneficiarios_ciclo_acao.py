import uuid

from acutis_api.communication.responses.agape import (
    GeolocalizacaoBeneficiarioResponse,
    ListarGeolocalizacoesBeneficiariosResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class ListarGeolocalizacoesBeneficiariosUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, ciclo_acao_id: uuid.UUID
    ) -> ListarGeolocalizacoesBeneficiariosResponse:
        """
        Executa a lógica para listar as geolocalizações dos beneficiários.
        """
        ciclo_acao = self.agape_repository.buscar_ciclo_acao_agape_por_id(
            ciclo_acao_id
        )
        if ciclo_acao is None:
            raise HttpNotFoundError('Ciclo de ação não encontrado.')

        familias_beneficiadas = (
            self.agape_repository.listar_geolocalizadores_familia_por_ciclo_id(
                ciclo_acao_id=ciclo_acao_id,
            )
        )

        geolocalizacoes_respostas = []
        if familias_beneficiadas:
            for familia in familias_beneficiadas:
                geolocalizacoes_respostas.append(
                    GeolocalizacaoBeneficiarioResponse.model_validate(
                        dict(familia._mapping)
                    )
                )

        return ListarGeolocalizacoesBeneficiariosResponse(
            ciclo_acao_id=ciclo_acao.id,
            resultados=geolocalizacoes_respostas,
        ).model_dump()
