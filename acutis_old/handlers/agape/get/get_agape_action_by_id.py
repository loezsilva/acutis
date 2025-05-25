from http import HTTPStatus
from typing import Dict, List
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.instancia_acao_agape import InstanciaAcaoAgape
from models.endereco import Endereco
from models.schemas.agape.get.get_agape_action_by_id import (
    AgapeActionAddressSchema,
    DonationSchema,
    GetAgapeActionByIdResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAgapeActionById:
    def __init__(self, repository: AgapeRepositoryInterface):
        self.__repository = repository

    def execute(self, fk_acao_agape_id: int):
        ultima_instancia = self.__get_last_agape_action_instance(
            fk_acao_agape_id
        )
        endereco = self.__get_agape_action_instance_address(
            ultima_instancia.id
        )
        doacoes = self.__get_agape_action_instance_donations(
            ultima_instancia.id
        )
        response = self.__prepare_response(endereco, doacoes, ultima_instancia)

        return response, HTTPStatus.OK

    def __get_last_agape_action_instance(
        self, fk_acao_agape_id: int
    ) -> InstanciaAcaoAgape:
        ultima_instancia = self.__repository.get_last_agape_action_instance(
            fk_acao_agape_id
        )
        if ultima_instancia is None:
            raise NotFoundError(
                "Última instância da ação ágape não encontrada."
            )
        return ultima_instancia

    def __get_agape_action_instance_address(
        self, instancia_acao_agape_id: int
    ) -> Endereco:
        endereco = self.__repository.get_agape_action_instance_address(
            instancia_acao_agape_id
        )
        return endereco

    def __get_agape_action_instance_donations(
        self, instancia_acao_agape_id: int
    ) -> List[DonationSchema]:
        doacoes = self.__repository.get_agape_action_instance_donations(
            instancia_acao_agape_id
        )
        return doacoes

    def __prepare_response(
        self,
        endereco: Endereco,
        doacoes: List[DonationSchema],
        ultima_instacia: InstanciaAcaoAgape,
    ) -> Dict:
        response = GetAgapeActionByIdResponse(
            abrangencia=ultima_instacia.abrangencia,
            endereco=AgapeActionAddressSchema.from_orm(endereco).dict(),
            doacoes=[
                DonationSchema.from_orm(doacao).dict() for doacao in doacoes
            ],
        ).dict()

        return response
