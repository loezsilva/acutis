from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.perfil import Perfil
from models.permissao_menu import PermissaoMenu
from models.schemas.admin.put.update_profile_permissions import (
    UpdateProfilePermissionsRequest,
)
from utils.functions import get_current_time


class UpdateProfilePermissions:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_perfil_id: int):
        profile = self.__get_profile_data(fk_perfil_id)
        request = UpdateProfilePermissionsRequest.parse_obj(flask_request.get_json())

        self.__update_profile_permissions(request, profile.id)
        self.__commit_changes()

        return {
            "msg": f"Permissões do perfil {profile.nome.capitalize()} atualizadas com sucesso!"
        }, 200

    def __get_profile_data(self, fk_perfil_id: int) -> Perfil:
        profile: Perfil = (
            self.__database.session.query(Perfil).filter_by(id=fk_perfil_id).first()
        )
        if profile is None:
            raise NotFoundError("Perfil não encontrado.")
        if (
            profile.nome.capitalize() == "Administrador"
            or profile.nome.capitalize() == "Benfeitor"
        ):
            raise ConflictError("Este perfil não pode ser editado.")

        return profile

    def __update_profile_permissions(
        self, menu: UpdateProfilePermissionsRequest, profile_id: int
    ):
        menu_permission = PermissaoMenu.query.filter_by(
            fk_perfil_id=profile_id, fk_menu_id=menu.fk_menu_id
        ).first()
        if not menu_permission:
            raise NotFoundError("Permissões de menu não encontrada.")

        if menu.acessar is not None:
            menu_permission.acessar = menu.acessar
        if menu.criar is not None:
            menu_permission.criar = menu.criar
        if menu.editar is not None:
            menu_permission.editar = menu.editar
        if menu.deletar is not None:
            menu_permission.deletar = menu.deletar
        menu_permission.data_alteracao = get_current_time()
        menu_permission.usuario_alteracao = current_user["id"]

    def __commit_changes(self):
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
