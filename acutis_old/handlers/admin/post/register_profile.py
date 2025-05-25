from typing import Optional
from flask import request as flask_request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_conflict import ConflictError
from models.menu_sistema import MenuSistema
from models.perfil import Perfil
from models.permissao_menu import PermissaoMenu
from models.schemas.admin.post.register_profile import RegisterProfileRequest
from utils.functions import is_valid_name


class RegisterProfile:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        request = RegisterProfileRequest.parse_obj(flask_request.json)
        nome = is_valid_name(request.nome.strip(), title=False)
        status = request.status
        super_perfil = request.super_perfil
        profile = self.__register_profile(nome, status, super_perfil)
        self.__init_permissions_to_profile(profile)
        self.__commit_changes()

        return {"msg": "Perfil cadastrado com sucesso!"}, 201

    def __register_profile(
        self, nome: str, status: Optional[bool], super_perfil: bool
    ) -> Perfil:
        
        perfil_ja_cadastrado = self.__database.session.query(Perfil).filter(Perfil.nome == nome).first()
        
        if perfil_ja_cadastrado != None:
            raise ConflictError("Perfil com nome já cadastrado.")
        
        profile = Perfil(
            nome=nome,
            status=status,
            super_perfil=super_perfil,
            usuario_criacao=current_user["id"],
        )
        self.__database.session.add(profile)
        self.__database.session.flush()

        return profile

    def __init_permissions_to_profile(self, profile: Perfil) -> None:
        menus = self.__database.session.query(MenuSistema.id).all()
        for menu in menus:
            menu_permission = PermissaoMenu(
                fk_menu_id=menu.id,
                fk_perfil_id=profile.id,
                acessar=False,
                criar=False,
                editar=False,
                deletar=False,
                usuario_criacao=current_user["id"],
            )
            self.__database.session.add(menu_permission)

    def __commit_changes(self):
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
