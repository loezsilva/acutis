from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.generais import Generais
from models.landpage_usuarios import LandpageUsers
from models.pedido import Pedido
from models.usuario import Usuario
from services.file_service import FileService
from templates.email_templates import delete_account_message_email_template
from utils.functions import get_current_time
from utils.send_email import send_email


class DeleteSelfAccount:
    def __init__(
        self, database: SQLAlchemy, file_service: FileService
    ) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        user = self.__get_user_data(current_user["id"])
        clifor = self.__get_clifor_data(user.id)
        self.__soft_delete_self_account(user, clifor.id)
        self.__send_email_delete_confirmation(user)
        self.__commit_changes()
        return {"msg": "Sua conta foi excluída com sucesso."}, 200

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
            raise NotFoundError("Dados do usuário não encontrados.")
        return clifor

    def __soft_delete_self_account(
        self, user: Usuario, clifor_id: int
    ) -> None:
        self.__database.session.query(Generais).filter(
            Generais.fk_usuario_id == user.id
        ).delete(synchronize_session=False)
        self.__database.session.query(LandpageUsers).filter(
            LandpageUsers.user_id == user.id
        ).delete(synchronize_session=False)

        user.deleted_at = get_current_time()
        if user.avatar:
            self.__file_service.delete_object(user.avatar)
        user.avatar = None
        user.nome_social = None
        self.__database.session.query(Pedido).filter(
            Pedido.fk_clifor_id == clifor_id
        ).update({Pedido.anonimo: True}, synchronize_session=False)

    def __send_email_delete_confirmation(self, user: Usuario) -> None:
        html = delete_account_message_email_template(user.nome)
        send_email(
            "Instituto Hesed - Confirmação de Exclusão de Cadastro",
            user.email,
            html,
            5,
        )

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
