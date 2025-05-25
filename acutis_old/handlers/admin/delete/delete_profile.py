from typing import List
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario


class DeleteProfile:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_perfil_id: int):
        profile = self.__get_profile_data(fk_perfil_id)
        self.__delete_profile_data(profile)
        self.__commit_changes()

        return {"msg": "Perfil deletado com sucesso!"}, 200

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
            raise ConflictError("Este perfil não pode ser deletado.")

        return profile

    def __delete_profile_data(self, profile: Perfil) -> None:
        default_profile: Perfil = Perfil.query.filter_by(nome="Benfeitor").first()
        change_profile_users: List[PermissaoUsuario] = PermissaoUsuario.query.filter_by(
            fk_perfil_id=profile.id
        ).all()
        for user in change_profile_users:
            user.fk_perfil_id = default_profile.id

        self.__database.session.delete(profile)

    def __commit_changes(self):
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
