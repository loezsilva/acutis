from typing import Dict, List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from exceptions.error_types.http_not_found import NotFoundError
from models.menu_sistema import MenuSistema
from models.perfil import Perfil
from models.permissao_menu import PermissaoMenu
from models.schemas.admin.get.get_by_id.get_profile_by_id import (
    GetPermissionsMenuProfileSchema,
    GetProfileByIdResponse,
    GetProfileByIdSchema,
)


class GetProfileById:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_perfil_id: int):
        profile = self.__get_profile_data(fk_perfil_id)
        menu_permissions = self.__get_menu_permissions_data(profile.id)
        response = self.__prepare_response(profile, menu_permissions)

        return response, 200

    def __get_profile_data(self, fk_perfil_id: int) -> Perfil:
        profile_query = self.__database.session.query(
            Perfil.id,
            Perfil.nome,
            Perfil.status,
            Perfil.super_perfil,
            func.format(Perfil.data_criacao, "dd/MM/yyyy").label("data_criacao"),
        ).filter(Perfil.id == fk_perfil_id)

        profile: Perfil = profile_query.first()

        if profile is None:
            raise NotFoundError("Perfil não encontrado.")

        return profile

    def __get_menu_permissions_data(self, fk_perfil_id: int) -> List[PermissaoMenu]:
        menu_permissions_query = (
            self.__database.session.query(
                PermissaoMenu.fk_menu_id,
                PermissaoMenu.acessar,
                PermissaoMenu.criar,
                PermissaoMenu.editar,
                PermissaoMenu.deletar,
                MenuSistema.menu.label("nome_menu"),
            )
            .join(MenuSistema, MenuSistema.id == PermissaoMenu.fk_menu_id)
            .filter(PermissaoMenu.fk_perfil_id == fk_perfil_id)
        )

        menu_permissions = menu_permissions_query.all()

        return menu_permissions

    def __prepare_response(
        self, profile: Perfil, menu_permissions: List[PermissaoMenu]
    ) -> Dict:
        profile_response = GetProfileByIdSchema.from_orm(profile).dict()
        response = GetProfileByIdResponse(
            perfil=profile_response,
            menus=[
                GetPermissionsMenuProfileSchema.from_orm(menu).dict()
                for menu in menu_permissions
            ],
        ).dict()

        return response
