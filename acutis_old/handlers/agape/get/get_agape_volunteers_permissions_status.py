from http import HTTPStatus
from models.permissao_menu import PermissaoMenu
from models.schemas.agape.get.get_agape_volunteers_permissions_status import (
    GetAgapeVolunteersPermissionsStatusResponse,
)
from repositories.agape_repository import AgapeRepository


class GetAgapeVolunteersPermissionsStatus:
    def __init__(self, repository: AgapeRepository) -> None:
        self.__repository = repository

    def execute(self):
        voluntario_agape = self.__repository.get_volunteer_profile()
        permissao_menu = self.__repository.get_volunteer_permission(
            voluntario_agape
        )
        response = self.__prepare_response(permissao_menu)

        return response, HTTPStatus.OK

    def __prepare_response(self, permissao_menu: PermissaoMenu) -> dict:
        response = GetAgapeVolunteersPermissionsStatusResponse(
            status=all(
                [
                    permissao_menu.acessar,
                    permissao_menu.criar,
                    permissao_menu.editar,
                ]
            )
        ).dict()

        return response
