from http import HTTPStatus
from typing import Dict, List
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.instancia_acao_agape import (
    InstanciaAcaoAgape,
)
from models.endereco import Endereco
from models.schemas.agape.get.get_instance_beneficiaries_addresses_geolocation import (
    BeneficiariesGeolocationsSchema,
    GeolocationSchema,
    GetInstanceBeneficiariesAddressesGeolocationResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetInstanceBeneficiariesAddressesGeolocation:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self, fk_instancia_acao_agape_id: int):
        instancia_acao_agape = self.__get_agape_action_instance_data(
            fk_instancia_acao_agape_id
        )
        endereco_instancia_agape = (
            self.__repository.get_agape_action_instance_address(
                instancia_acao_agape.id
            )
        )
        geolocalizacoes_beneficiarios = (
            self.__get_instance_beneficiaries_addresses(
                instancia_acao_agape.id
            )
        )
        response = self.__prepare_response(
            endereco_instancia_agape, geolocalizacoes_beneficiarios
        )

        return response, HTTPStatus.OK

    def __get_agape_action_instance_data(
        self, fk_instancia_acao_agape_id: int
    ) -> InstanciaAcaoAgape:
        instancia_acao_agape: InstanciaAcaoAgape = (
            self.__repository.get_agape_action_instance_by_id(
                fk_instancia_acao_agape_id
            )
        )
        if instancia_acao_agape is None:
            raise NotFoundError("Ciclo de ação ágape não encontrado.")

        return instancia_acao_agape

    def __get_instance_beneficiaries_addresses(
        self, fk_instancia_acao_agape_id: int
    ):
        geolocalizacoes_beneficiarios = (
            self.__repository.get_instance_beneficiaries_geolocations(
                fk_instancia_acao_agape_id
            )
        )

        return geolocalizacoes_beneficiarios

    def __prepare_response(
        self,
        endereco_instancia_agape: Endereco,
        geolocalizacoes: List[BeneficiariesGeolocationsSchema],
    ) -> Dict:
        response = GetInstanceBeneficiariesAddressesGeolocationResponse(
            ciclo_acao_agape=GeolocationSchema.from_orm(
                endereco_instancia_agape
            ).dict(),
            beneficiarios=[
                BeneficiariesGeolocationsSchema.from_orm(geolocalizacao).dict()
                for geolocalizacao in geolocalizacoes
            ],
        ).dict()

        return response
