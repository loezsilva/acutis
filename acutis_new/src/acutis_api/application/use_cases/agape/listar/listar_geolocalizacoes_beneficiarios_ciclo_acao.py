import uuid
from http import HTTPStatus

from acutis_api.communication.responses.agape import (
    ListarGeolocalizacoesBeneficiariosResponse,
    GeolocalizacaoBeneficiarioResponse,
)
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface

class ListarGeolocalizacoesBeneficiariosUseCase:
    """
    Caso de uso para listar as geolocalizações dos beneficiários de um ciclo de ação ágape.
    """

    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    def execute(
        self, ciclo_acao_id: uuid.UUID
    ) -> tuple[ListarGeolocalizacoesBeneficiariosResponse, HTTPStatus]:
        """
        Executa a lógica para listar as geolocalizações dos beneficiários.
        """
        familias_beneficiadas = (
            self.agape_repository.\
                listar_familias_beneficiadas_por_ciclo_acao_id(
                ciclo_acao_id=ciclo_acao_id
            )
        )

        geolocalizacoes_list = []
        if familias_beneficiadas:
            for familia_entity in familias_beneficiadas:
                if familia_entity.fk_endereco_id:
                    if endereco := self.agape_repository.\
                        buscar_endereco_por_id(
                        familia_entity.fk_endereco_id
                    ):
                        if coordenada := endereco.coordenada:

                            if (
                                coordenada.latitude is not None 
                                and coordenada.longitude is not None
                            ):
                                geolocalizacoes_list.append(
                                    GeolocalizacaoBeneficiarioResponse(
                                        familia_id=familia_entity.id,
                                        nome_familia=(
                                            familia_entity.nome_familia
                                        ),
                                        latitude=coordenada.latitude,
                                        longitude=coordenada.longitude,
                                        endereco_id=familia_entity.endereco.id,
                                    )
                                )
        
        return ListarGeolocalizacoesBeneficiariosResponse(
            root=geolocalizacoes_list
        ), HTTPStatus.OK