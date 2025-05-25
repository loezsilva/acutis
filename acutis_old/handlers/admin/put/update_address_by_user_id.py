from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.endereco import Endereco
from models.schemas.admin.put.update_address_by_user_id import (
    UpdateAddressByUserIdRequest,
)
from models.usuario import Usuario
from utils.functions import get_current_time


class UpdateAddressByUserId:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_usuario_id: int):
        req = UpdateAddressByUserIdRequest.parse_obj(request.get_json())
        address = self.__get_user_address(fk_usuario_id)
        self.__update_address(address, req)
        self.__commit_changes()

        return {"msg": "Endereço atualizado com sucesso"}, 200

    def __get_user_address(self, fk_usuario_id: int) -> Endereco:
        address = (
            Endereco.query.select_from(Usuario)
            .join(Clifor, Usuario.id == Clifor.fk_usuario_id)
            .join(Endereco, Clifor.id == Endereco.fk_clifor_id)
            .filter(Usuario.id == fk_usuario_id, Usuario.deleted_at.is_(None))
        ).first()

        if address is None:
            raise NotFoundError("Endereço não encontrado.")

        return address

    def __update_address(
        self, address: Endereco, req: UpdateAddressByUserIdRequest
    ) -> None:
        address.cep = req.cep
        address.rua = req.rua
        address.numero = req.numero
        address.complemento = req.complemento
        address.ponto_referencia = req.ponto_referencia
        address.bairro = req.bairro
        address.estado = req.estado
        address.cidade = req.cidade
        address.detalhe_estrangeiro = req.detalhe_estrangeiro
        address.obriga_atualizar_endereco = False
        address.ultima_atualizacao_endereco = get_current_time().date()
        address.usuario_alteracao = current_user["id"]
        address.data_alteracao = get_current_time()

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
