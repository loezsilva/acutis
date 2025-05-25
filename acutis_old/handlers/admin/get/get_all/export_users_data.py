from typing import Callable, List

from models.schemas.admin.get.get_all.export_users_data import (
    ExportUsersDataCSV,
)
from models.usuario import Usuario
from repositories.interfaces.admin_repository_interface import (
    AdminRepositoryInterface,
)


class ExportUsersData:
    def __init__(
        self,
        admin_repository: AdminRepositoryInterface,
        export_excel: Callable,
    ) -> None:
        self.__admin_repository = admin_repository
        self.__export_excel = export_excel

    def execute(self):
        users = self.__get_all_users_data()
        response = self.__prepare_response(users)

        return response, 200

    def __get_all_users_data(self) -> List[Usuario]:
        users = self.__admin_repository.get_all_regular_users()
        return users

    def __prepare_response(self, users: List[Usuario]) -> dict:
        csv_data = [ExportUsersDataCSV.from_orm(user).dict() for user in users]

        response = self.__export_excel(csv_data, "dados_usuarios")
        return response
