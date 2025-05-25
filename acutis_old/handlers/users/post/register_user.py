from typing import Literal, Optional
from flask_sqlalchemy import SQLAlchemy
from flask import request

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError


from handlers.users.post.interfaces.register_anonymous_user_interface import (
    RegisterAnonymousUserInterface,
)
from handlers.users.post.interfaces.register_deleted_user_interface import (
    RegisterDeletedUserInterface,
)
from models.campanha import Campanha
from models.clifor import Clifor
from models.endereco import Endereco
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.schemas.users.post.register_user import RegisterUserRequest
from models.users_imports import UsersImports
from models.usuario import Usuario
from services.send_data_to_app_acutis import SendDataToAppAcutis
from templates.email_templates import active_account_email_template
from utils.functions import get_current_time, is_valid_email, is_valid_name
from utils.regex import format_string, validate_password
from utils.send_email import send_email
from utils.token_email import generate_token
from utils.validator import cpf_cnpj_validator


class RegisterUser:
    def __init__(
        self,
        database: SQLAlchemy,
        register_deleted_user: RegisterDeletedUserInterface,
        register_anonymous_user: RegisterAnonymousUserInterface,
    ) -> None:
        self.__database = database
        self.__register_deleted_user = register_deleted_user
        self.__register_anonymous_user = register_anonymous_user

    def execute(self):
        register_user = RegisterUserRequest.parse_obj(request.json)
        pais = register_user.pais.strip()
        nome = is_valid_name(register_user.nome.strip())
        email = is_valid_email(
            register_user.email.strip(),
            check_deliverability=True,
            check_valid_domain=True,
        )
        password = validate_password(register_user.password.get_secret_value().strip())
        campanha_origem = self.__validate_origin_campaign(register_user.campanha_origem)
        tipo_documento = register_user.tipo_documento.strip()
        numero_documento = cpf_cnpj_validator(
            register_user.numero_documento.strip(), tipo_documento
        )

        user_type_registering = self.__get_user_type_registering(
            numero_documento, tipo_documento
        )

        clifor = self.__get_clifor_data(numero_documento)

        if user_type_registering == "deleted_user":
            user = self.__database.session.get(Usuario, clifor.fk_usuario_id)
            return self.__register_deleted_user.register(
                database=self.__database,
                usuario=user,
                clifor=clifor,
                pais=pais,
                nome=nome,
                email=email,
                password=password,
                campanha_origem=campanha_origem,
            )

        self.__validate_email_in_use(email)
        profile = self.__get_profile("Benfeitor")
        origem_cadastro = self.__get_user_is_import(email)

        if user_type_registering == "anonymous_user":
            return self.__register_anonymous_user.register(
                database=self.__database,
                clifor=clifor,
                profile=profile,
                pais=pais,
                nome=nome,
                email=email,
                password=password,
                numero_documento=numero_documento,
                campanha_origem=campanha_origem,
                origem_cadastro=origem_cadastro,
            )

        user = self.__register_user_data(
            pais, nome, email, password, origem_cadastro, campanha_origem
        )
        clifor = self.__register_clifor_data(user, nome, numero_documento, email)
        self.__register_user_address_data(clifor.id, pais)
        self.__register_user_permissions(user, profile)
        self.__send_email_confirmation_account(email, nome, campanha_origem)
        self.__commit_changes()

        if register_user.campanha_origem == 43:
            # envia dados do usuário para o app acutis quando cadastro realizado na campanha 43
            payload = {
                "email": clifor.email,
                "cpf": clifor.cpf_cnpj,
                "patent": "membro",
                "name": clifor.nome
            }
                        
            register_general_in_app_acutis = SendDataToAppAcutis(payload)
            register_general_in_app_acutis.execute()

        return {"msg": "Usuário cadastrado com sucesso."}, 201

    def __validate_origin_campaign(self, origem_campanha: int) -> None:
        if origem_campanha and not self.__database.session.get(
            Campanha, origem_campanha
        ):
            raise NotFoundError("Campanha não encontrada.")

        return origem_campanha

    def __get_user_type_registering(
        self, numero_documento: str, tipo_documento: str
    ) -> Literal["deleted_user", "anonymous_user", "new_user"]:
        clifor = Clifor.query.filter_by(cpf_cnpj=numero_documento).first()
        if clifor:
            if clifor.fk_usuario_id:
                usuario = self.__database.session.get(Usuario, clifor.fk_usuario_id)
                if usuario.deleted_at is not None:
                    return "deleted_user"

                raise ConflictError(
                    f"{format_string(tipo_documento.title(), lower=False)} já cadastrado."
                )

            return "anonymous_user"
        return "new_user"

    def __get_clifor_data(self, numero_documento: str) -> Optional[Clifor]:
        clifor: Clifor = Clifor.query.filter_by(cpf_cnpj=numero_documento).first()

        return clifor

    def __validate_email_in_use(self, email: str) -> None:
        email_already_registered = Usuario.query.filter_by(email=email).first()
        if email_already_registered:
            raise ConflictError("Email já cadastrado.")

    def __get_profile(self, profile_name: str) -> Perfil:
        profile = Perfil.query.filter(Perfil.nome.ilike(profile_name)).first()
        if profile is None:
            raise NotFoundError("Perfil não encontrado.")
        return profile

    def __get_user_is_import(self, email: str) -> Optional[int]:
        user_import: UsersImports = UsersImports.query.filter_by(email=email).first()
        return user_import.origem_cadastro if user_import else None

    def __register_user_data(
        self,
        pais: str,
        nome: str,
        email: str,
        password: str,
        origem_cadastro: Optional[int],
        campanha_origem: Optional[int],
    ) -> Usuario:

        user = Usuario(
            nome=nome,
            email=email,
            password=password,
            country=pais,
            campanha_origem=campanha_origem,
            origem_cadastro=origem_cadastro,
            data_inicio=get_current_time(),
            obriga_atualizar_cadastro=True,
        )

        self.__database.session.add(user)
        self.__database.session.flush()

        return user

    def __register_clifor_data(
        self,
        user: Usuario,
        nome: str,
        numero_documento: str,
        email: str,
    ) -> Clifor:

        clifor = Clifor(
            fk_usuario_id=user.id,
            nome=nome,
            cpf_cnpj=numero_documento,
            email=email,
            usuario_criacao=user.id,
        )
        self.__database.session.add(clifor)
        self.__database.session.flush()

        return clifor

    def __register_user_address_data(self, clifor_id: int, pais: str) -> None:
        address = Endereco(
            fk_clifor_id=clifor_id, obriga_atualizar_endereco=True, pais_origem=pais
        )
        self.__database.session.add(address)

    def __register_user_permissions(self, user: Usuario, profile: Perfil) -> None:
        user_permission = PermissaoUsuario(
            fk_usuario_id=user.id, fk_perfil_id=profile.id, usuario_criacao=user.id
        )
        self.__database.session.add(user_permission)

    def __send_email_confirmation_account(
        self, email: str, nome: str, campanha_origem: Optional[int]
    ) -> None:
        payload = {"email": email, "campanha_origem": campanha_origem}
        token = generate_token(obj=payload, salt="active_account_confirmation")
        html = active_account_email_template(nome, token)
        send_email("HeSed - Verificação de Email", email, html, 1)

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
