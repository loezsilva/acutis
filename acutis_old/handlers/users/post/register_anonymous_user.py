from typing import Optional
from flask_sqlalchemy import SQLAlchemy

from handlers.users.post.interfaces.register_anonymous_user_interface import (
    RegisterAnonymousUserInterface,
)
from models.clifor import Clifor
from models.endereco import Endereco
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.usuario import Usuario
from services.send_data_to_app_acutis import SendDataToAppAcutis
from templates.email_templates import active_account_email_template
from utils.functions import get_current_time
from utils.send_email import send_email
from utils.token_email import generate_token


class RegisterAnonymousUser(RegisterAnonymousUserInterface):
    def register(
        self,
        database: SQLAlchemy,
        clifor: Clifor,
        profile: Perfil,
        pais: str,
        nome: str,
        email: str,
        password: str,
        numero_documento: str,
        campanha_origem: Optional[int],
        origem_cadastro: Optional[int],
    ):
        user = self.__register_user_data(
            database, pais, nome, email, password, campanha_origem, origem_cadastro
        )

        self.__register_clifor_data(clifor, user, nome, numero_documento, email)
        self.__register_user_address_data(database, clifor.id, pais)
        self.__register_user_permissions(database, user, profile)
        self.__send_email_confirmation_account(email, nome, campanha_origem)
        self.__commit_changes(database)
        
        if campanha_origem == 43:
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

    def __register_user_data(
        self,
        database: SQLAlchemy,
        pais: str,
        nome: str,
        email: str,
        password: str,
        campanha_origem: Optional[int],
        origem_cadastro: Optional[int],
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

        database.session.add(user)
        database.session.flush()

        return user

    def __register_clifor_data(
        self,
        clifor: Clifor,
        user: Usuario,
        nome: str,
        numero_documento: str,
        email: str,
    ) -> None:

        clifor.fk_usuario_id = user.id
        clifor.nome = nome
        clifor.cpf_cnpj = numero_documento
        clifor.email = email
        clifor.usuario_criacao = user.id

    def __register_user_address_data(
        self, database: SQLAlchemy, clifor_id: int, pais: str
    ) -> None:
        address = Endereco(
            fk_clifor_id=clifor_id, obriga_atualizar_endereco=True, pais_origem=pais
        )
        database.session.add(address)

    def __register_user_permissions(
        self, database: SQLAlchemy, user: Usuario, profile: Perfil
    ) -> None:
        user_permission = PermissaoUsuario(
            fk_usuario_id=user.id, fk_perfil_id=profile.id, usuario_criacao=user.id
        )
        database.session.add(user_permission)

    def __send_email_confirmation_account(
        self, email: str, nome: str, campanha_origem: Optional[int]
    ) -> None:
        payload = {"email": email, "campanha_origem": campanha_origem}
        token = generate_token(obj=payload, salt="active_account_confirmation")
        html = active_account_email_template(nome, token)
        send_email("HeSed - Verificação de Email", email, html, 1)

    def __commit_changes(self, database: SQLAlchemy) -> None:
        try:
            database.session.commit()
        except Exception as exception:
            database.session.rollback()
            raise exception
