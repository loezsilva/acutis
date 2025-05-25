from http import HTTPStatus
from typing import Dict
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.instancia_acao_agape import InstanciaAcaoAgape
from models.endereco import Endereco
from models.schemas.agape.get.get_agape_instance_address import (
    GetAgapeInstanceAddressResponse,
)
from repositories.interfaces.agape_repository_interface import (
    AgapeRepositoryInterface,
)


class GetAgapeInstanceAddress:
    def __init__(self, repository: AgapeRepositoryInterface) -> None:
        self.__repository = repository

    def execute(self, fk_instancia_acao_agape_id: int):
        instancia_acao_agape = self.__get_agape_action_instance_data(
            fk_instancia_acao_agape_id
        )
        endereco = self.__repository.get_agape_action_instance_address(
            fk_instancia_acao_agape_id
        )
        response = self.__prepare_response(instancia_acao_agape, endereco)

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
        self, instancia_acao_agape: InstanciaAcaoAgape, endereco: Endereco
    ) -> Dict:
        response = GetAgapeInstanceAddressResponse(
            cep=endereco.cep,
            rua=endereco.rua,
            bairro=endereco.bairro,
            cidade=endereco.cidade,
            estado=endereco.estado,
            numero=endereco.numero,
            complemento=endereco.complemento,
            abrangencia=instancia_acao_agape.abrangencia,
        ).dict()
        return response
