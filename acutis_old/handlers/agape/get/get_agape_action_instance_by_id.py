from http import HTTPStatus
from typing import Dict, List
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.instancia_acao_agape import InstanciaAcaoAgape
from models.endereco import Endereco
from models.schemas.agape.get.get_agape_action_instance_by_id import (
    AgapeActionAddressSchema,
    DonationSchema,
    GetAgapeActionInstanceByIdResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAgapeActionInstanceById:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self, fk_instancia_acao_agape_id: int):
        instancia_acao_agape = self.__get_agape_action_instance_data(
            fk_instancia_acao_agape_id
        )
        endereco = self.__repository.get_agape_action_instance_address(
            fk_instancia_acao_agape_id
        )
        doacoes = self.__repository.get_agape_action_instance_donations(
            fk_instancia_acao_agape_id
        )
        response = self.__prepare_response(
            endereco, doacoes, instancia_acao_agape
        )

        return response, HTTPStatus.OK

    def __get_agape_action_instance_data(
        self, fk_instancia_acao_agape_id: int
    ):
        instancia_acao_agape = (
            self.__repository.get_agape_action_instance_by_id(
                fk_instancia_acao_agape_id
            )
        )
        if instancia_acao_agape is None:
            raise NotFoundError("Ciclo de ação ágape não encontrado.")

        return instancia_acao_agape

    def __prepare_response(
        self,
        endereco: Endereco,
        doacoes: List[DonationSchema],
        instancia_acao_agape: InstanciaAcaoAgape,
    ) -> Dict:
        response = GetAgapeActionInstanceByIdResponse(
            fk_acao_agape_id=instancia_acao_agape.fk_acao_agape_id,
            abrangencia=instancia_acao_agape.abrangencia,
            endereco=AgapeActionAddressSchema.from_orm(endereco).dict(),
            doacoes=[
                DonationSchema.from_orm(doacao).dict() for doacao in doacoes
            ],
        ).dict()

        return response
