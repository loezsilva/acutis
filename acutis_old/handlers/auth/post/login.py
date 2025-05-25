from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from exceptions.error_types.http_unauthorized import UnauthorizedError
from models.campanha import Campanha
from models.foto_campanha import FotoCampanha
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.schemas.auth.post.login import LoginRequest
from models.usuario import Usuario
from templates.email_templates import active_account_email_template
from utils.functions import get_current_time, is_valid_email
from utils.send_email import send_email
from utils.token_email import generate_token


class Login:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        req = LoginRequest.parse_obj(request.get_json())

        email = is_valid_email(
            req.email.strip(), check_deliverability=False, check_valid_domain=False
        )
        password = req.password.strip()
        update_photo = False

        user = self.__search_user_in_database(email)
        self.__verify_user_password(user, password)
        self.__verify_user_status(user)
        self.__verify_profile_is_active(user)

        if user.campanha_origem:
            update_photo = self.__check_needs_update_photo_origin_campaign(user)

        self.__register_log_user_access(user, update_photo)
        response = self.__prepare_response(user)

        return response, 200

    def __search_user_in_database(self, email: str) -> Usuario:
        user: Usuario = Usuario.query.filter_by(email=email, deleted_at=None).first()
        if user is None:
            raise NotFoundError(
                "Usuário não encontrado. Por favor, cadastre-se para prosseguir!"
            )
        return user

    def __verify_user_password(self, user: Usuario, password: str) -> None:
        if user.verify_password(password) is False:
            raise UnauthorizedError("O email ou a senha estão incorretos.")

    def __send_email_active_user_account(self, user: Usuario) -> None:
        payload = {"email": user.email}
        token = generate_token(obj=payload, salt="active_account_confirmation")
        html = active_account_email_template(user.nome, token)
        send_email("HeSed - Verificação de Email", user.email, html, 1)

    def __verify_user_status(self, user: Usuario) -> None:
        if user.status is False:
            self.__send_email_active_user_account(user)
            raise UnauthorizedError(
                "Ative sua conta acessando o link enviado para seu email, antes de logar!"
            )

        if user.bloqueado:
            raise UnauthorizedError(
                "Sua conta está bloqueada! Entre em contato com o time de suporte."
            )

    def __verify_profile_is_active(self, user: Usuario) -> None:
        profile: Perfil = (
            self.__database.session.query(Perfil.status, Perfil.nome)
            .select_from(Usuario)
            .join(PermissaoUsuario, Usuario.id == PermissaoUsuario.fk_usuario_id)
            .join(Perfil, PermissaoUsuario.fk_perfil_id == Perfil.id)
            .filter(Usuario.id == user.id)
            .first()
        )

        if profile.status is False:
            raise UnauthorizedError(
                f"Não foi possível efetuar o login. Perfil {profile.nome} inativo."
            )

    def __check_needs_update_photo_origin_campaign(self, user: Usuario) -> bool:
        campanha: Campanha = self.__database.session.get(Campanha, user.campanha_origem)
        if campanha is None:
            raise NotFoundError("Campanha não encontrada.")

        if campanha.preenchimento_foto:
            foto_campanha = FotoCampanha.query.filter_by(fk_usuario_id=user.id).first()
            if foto_campanha is None:
                return True
        return False

    def __register_log_user_access(self, user: Usuario, update_photo: bool) -> None:
        user.data_ultimo_acesso = get_current_time()
        if update_photo:
            user.obriga_atualizar_cadastro = True

        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

    def __prepare_response(self, user: Usuario) -> dict:
        response = {
            "access_token": create_access_token(identity=user.id),
            "refresh_token": create_refresh_token(identity=user.id),
            "type_token": "Bearer",
        }

        return response
