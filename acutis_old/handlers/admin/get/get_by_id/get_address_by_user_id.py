from typing import Tuple

from flask_sqlalchemy import SQLAlchemy


from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.endereco import Endereco
from models.schemas.admin.get.get_by_id.get_address_user_by_id import (
    GetAddressByUserIdResponse,
)
from models.usuario import Usuario


class GetAddressByUserId:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_usuario_id: int) -> Tuple:
        address = self.__get_user_address(fk_usuario_id)
        response = self.__prepare_response(address)

        return response, 200

    def __get_user_address(self, fk_usuario_id: int) -> Endereco:
        address = (
            self.__database.session.query(Endereco)
            .select_from(Usuario)
            .join(Clifor, Usuario.id == Clifor.fk_usuario_id)
            .join(Endereco, Clifor.id == Endereco.fk_clifor_id)
            .filter(Usuario.id == fk_usuario_id, Usuario.deleted_at.is_(None))
        ).first()

        if address is None:
            raise NotFoundError("Endereço não encontrado.")

        return address

    def __prepare_response(self, address: Endereco) -> dict:
        response = GetAddressByUserIdResponse.from_orm(address).dict()

        return response
