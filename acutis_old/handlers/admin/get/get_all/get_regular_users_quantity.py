from typing import Dict, Tuple

from repositories.interfaces.admin_repository_interface import (
    AdminRepositoryInterface,
)


class GetRegularUsersQuantity:
    def __init__(self, admin_repository: AdminRepositoryInterface) -> None:
        self.__admin_repository = admin_repository

    def execute(self) -> Tuple[Dict, int]:
        qtd_users = self.__get_regular_users_quantity()
        return {"qtd_usuarios": qtd_users}, 200

    def __get_regular_users_quantity(self) -> int:
        qtd_users = self.__admin_repository.get_regular_users_quantity()

        return qtd_users
