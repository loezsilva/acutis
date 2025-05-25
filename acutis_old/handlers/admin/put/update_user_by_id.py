from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.schemas.admin.put.update_user_by_id import UpdateUserByIdRequest
from models.usuario import Usuario
from utils.functions import get_current_time, is_valid_email, is_valid_name
from utils.regex import format_string


class UpdateUserById:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_usuario_id: int):
        user = self.__get_user_data(fk_usuario_id)
        clifor = self.__get_clifor_data(user.id)
        req = UpdateUserByIdRequest.parse_obj(request.get_json())
        pais = req.pais.strip()
        nome = is_valid_name(req.nome.strip())
        telefone = format_string(req.telefone.strip(), only_digits=True)
        email = is_valid_email(
            req.email.strip(),
            check_deliverability=True,
            check_valid_domain=True,
        )

        self.__is_email_already_in_use(email, clifor)

        self.__update_user_data(
            user=user,
            clifor=clifor,
            pais=pais,
            nome=nome,
            telefone=telefone,
            email=email,
        )

        self.__commit_changes()

        return {"msg": "Usuário atualizado com sucesso"}, 200

    def __get_user_data(self, fk_usuario_id: int) -> Usuario:
        user: Usuario = Usuario.query.filter_by(
            id=fk_usuario_id, deleted_at=None
        ).first()
        if user is None:
            raise NotFoundError("Usuário não encontrado.")

        return user

    def __get_clifor_data(self, user_id: int) -> Clifor:
        clifor = Clifor.query.filter_by(fk_usuario_id=user_id).first()
        if clifor is None:
            raise NotFoundError("Clifor não encontrado.")

        return clifor

    def __is_email_already_in_use(self, email: str, clifor: Clifor) -> None:
        is_email_registered: Clifor = Clifor.query.filter(Clifor.email == email).first()
        if is_email_registered and is_email_registered.id != clifor.id:
            raise ConflictError("Email já cadastrado.")

    def __update_user_data(
        self,
        user: Usuario,
        clifor: Clifor,
        pais: str,
        nome: str,
        telefone: str,
        email: str,
    ) -> None:
        if email != user.email:
            user.email = email
            clifor.email = email
            user.status = False

        user.country = pais
        user.nome = nome
        user.data_alteracao = get_current_time()
        user.usuario_alteracao = current_user["id"]

        clifor.nome = nome
        clifor.data_alteracao = get_current_time()
        clifor.usuario_alteracao = current_user["id"]

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
