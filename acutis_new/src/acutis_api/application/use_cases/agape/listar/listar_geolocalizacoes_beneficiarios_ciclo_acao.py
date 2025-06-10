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
            self.agape_repository.listar_familias_beneficiadas_por_ciclo_id(
                ciclo_acao_id=ciclo_acao_id
            )
        )

        geolocalizacoes_list = []
        if familias_beneficiadas:
            for familia_entity in familias_beneficiadas:
                if familia_entity.fk_endereco_id:
                    endereco = self.agape_repository.buscar_endereco_por_id(
                        familia_entity.fk_endereco_id
                    )
                    if endereco and endereco.coordenada:
                        coordenada = endereco.coordenada
                        geolocalizacoes_list.append(
                            GeolocalizacaoBeneficiarioResponse(
                                familia_id=familia_entity.id,
                                nome_familia=(familia_entity.nome_familia),
                                latitude=coordenada.latitude,
                                longitude=coordenada.longitude,
                                endereco_id=familia_entity.fk_endereco_id,
                            )
                        )

        return ListarGeolocalizacoesBeneficiariosResponse(
            root=geolocalizacoes_list
        ).model_dump()
