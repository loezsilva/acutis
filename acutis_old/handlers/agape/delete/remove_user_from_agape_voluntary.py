from http import HTTPStatus
from repositories.agape_repository import AgapeRepository


class RemoveUserFromAgapeVoluntary:
    def __init__(self, repository: AgapeRepository) -> None:
        self.__repository = repository

    def execute(self, fk_usuario_id: int) -> None:
        self.__repository.remove_user_from_agape_voluntary_profile(
            fk_usuario_id
        )
        return {}, HTTPStatus.NO_CONTENT
