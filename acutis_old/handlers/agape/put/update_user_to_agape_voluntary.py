from http import HTTPStatus
from repositories.agape_repository import AgapeRepository


class UpdateUserToAgapeVoluntary:
    def __init__(self, repository: AgapeRepository):
        self.__repository = repository

    def execute(self, fk_usuario_id: int):
        self.__repository.update_user_profile_to_agape_voluntary(fk_usuario_id)
        return {}, HTTPStatus.NO_CONTENT
