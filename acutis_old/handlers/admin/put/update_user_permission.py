from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unprocessable_entity import HttpUnprocessableEntity
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.schemas.admin.put.update_user_permission import UpdateUserPermissionRequest
from models.usuario import Usuario
from utils.functions import get_current_time


class UpdateUserPermission:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_usuario_id: int):
        req = UpdateUserPermissionRequest.parse_obj(request.json)
        self.__check_if_user_exists(fk_usuario_id)
        self.__check_if_profile_exists(req.fk_perfil_id)
        self.__update_user_permission(fk_usuario_id, req.fk_perfil_id)
        self.__commit_changes()

        return {"msg": "Permissão de usuário atualizada com sucesso!"}, 200

    def __check_if_user_exists(self, fk_usuario_id: int):
        user = Usuario.query.filter_by(id=fk_usuario_id, deleted_at=None).first()
        if user is None:
            raise NotFoundError("Usuário não encontrado.")

    def __check_if_profile_exists(self, fk_perfil_id: int):
        profile: Perfil = Perfil.query.filter_by(id=fk_perfil_id).first()
        if profile is None:
            raise NotFoundError("Perfil não encontrado.")

        if profile.status == False:
            raise HttpUnprocessableEntity("O Perfil está desativado.")

    def __update_user_permission(self, fk_usuario_id: int, fk_perfil_id: int):
        user_permission: PermissaoUsuario = PermissaoUsuario.query.filter_by(
            fk_usuario_id=fk_usuario_id
        ).first()
        if user_permission is None:
            raise NotFoundError("Permissão de usuário não encontrada.")

        user_permission.fk_perfil_id = fk_perfil_id
        user_permission.data_alteracao = get_current_time()
        user_permission.usuario_alteracao = current_user["id"]

    def __commit_changes(self):
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
