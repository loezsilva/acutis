
from http import HTTPStatus
from repositories.agape_repository import AgapeRepository


class UpdateAgapeVolunteersPermissions:
    def __init__(self, repository: AgapeRepository) -> None:
        self.__repository = repository

    def execute(self):
        perfil_voluntario = self.__repository.get_volunteer_profile()
        permissao = self.__repository.get_volunteer_permission(
            perfil_voluntario
        )
        self.__repository.update_volunteer_permission(permissao)

        return {}, HTTPStatus.NO_CONTENT
