from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_forbidden import ForbiddenError
from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.pedido import Pedido
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.usuario import Usuario
from services.file_service import FileService
from templates.email_templates import delete_account_message_email_template
from utils.functions import get_current_time
from utils.send_email import send_email


class DeleteUserById:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self, fk_usuario_id: int):
        user = self.__get_user_data(fk_usuario_id)
        self.__validate_account_can_be_deleted(user.id)
        clifor = self.__get_clifor_data(user.id)
        self.__soft_delete_user_data(user, clifor.id)
        self.__send_email_delete_confirmation(user)
        self.__commit_changes()

        return {"msg": "Usuário deletado com sucesso."}, 200

    def __get_user_data(self, fk_usuario_id: int) -> Usuario:
        user: Usuario = Usuario.query.filter_by(
            id=fk_usuario_id, deleted_at=None
        ).first()
        if user is None:
            raise BadRequestError("Usuário não encontrado.")

        return user

    def __validate_account_can_be_deleted(self, user_id: int) -> None:
        perfil = (
            self.__database.session.query(Perfil)
            .join(PermissaoUsuario, Perfil.id == PermissaoUsuario.fk_perfil_id)
            .join(Usuario, Usuario.id == PermissaoUsuario.fk_usuario_id)
            .filter(Usuario.id == user_id)
            .first()
        )
        if perfil is None:
            raise NotFoundError("Perfil do usuário não encontrada.")

        if (
            perfil.nome == "Administrador"
            and current_user["nome_perfil"] != "Administrador"
        ):
            raise ForbiddenError("Você não tem permissão para realizar esta ação.")

    def __get_clifor_data(self, user_id: int) -> Clifor:
        clifor = Clifor.query.filter_by(fk_usuario_id=user_id).first()
        if clifor is None:
            raise BadRequestError("Dados do usuário não encontrados.")

        return clifor

    def __soft_delete_user_data(self, user: Usuario, clifor_id: int) -> None:
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
            "Instituto Hesed - Confirmação de Exclusão de Cadastro", user.email, html, 5
        )

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
