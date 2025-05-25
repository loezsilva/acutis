from typing import Optional
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from handlers.users.post.interfaces.register_deleted_user_interface import (
    RegisterDeletedUserInterface,
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


class RegisterDeletedUser(RegisterDeletedUserInterface):
    def register(
        self,
        database: SQLAlchemy,
        usuario: Usuario,
        clifor: Clifor,
        pais: str,
        nome: str,
        email: str,
        password: str,
        campanha_origem: Optional[int],
    ):
        self.__validate_email_in_use(email, usuario.id)
        self.__reset_user_address(database, clifor.id, pais)
        self.__register_user_deleted(
            usuario,
            clifor,
            pais,
            nome,
            email,
            password,
            campanha_origem=campanha_origem,
        )
        self.__register_user_permissions(usuario.id)
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

    def __validate_email_in_use(self, email: str, usuario_id: int) -> None:
        valid_email = Usuario.query.filter_by(email=email).first()
        if valid_email and valid_email.id != usuario_id:
            raise ConflictError("Email já cadastrado.")

    def __reset_user_address(
        self, database: SQLAlchemy, clifor_id: int, pais: str
    ) -> None:
        address = Endereco.query.filter_by(fk_clifor_id=clifor_id).first()
        if address is None:
            address = Endereco(fk_clifor_id=clifor_id, obriga_atualizar_endereco=True)
            database.session.add(address)
            return

        address.rua = None
        address.numero = None
        address.complemento = None
        address.bairro = None
        address.cidade = None
        address.estado = None
        address.cep = None
        address.obriga_atualizar_endereco = True
        address.detalhe_estrangeiro = None
        address.pais_origem = pais
        address.fk_general_id = None

    def __register_user_deleted(
        self,
        usuario: Usuario,
        clifor: Clifor,
        pais: str,
        nome: str,
        email: str,
        password: str,
        campanha_origem: Optional[int],
    ) -> None:

        usuario.nome = nome
        usuario.email = email
        usuario.password = password
        usuario.country = pais
        usuario.campanha_origem = campanha_origem
        usuario.status = False
        usuario.deleted_at = None
        usuario.data_inicio = get_current_time()
        usuario.obriga_atualizar_cadastro = True

        clifor.nome = nome
        clifor.email = email
        clifor.data_nascimento = None
        clifor.sexo = None

    def __register_user_permissions(self, user_id: int) -> None:
        profile = Perfil.query.filter(Perfil.nome.ilike("Benfeitor")).first()
        if profile is None:
            raise NotFoundError("Perfil não encontrado.")

        user_permission = PermissaoUsuario.query.filter_by(
            fk_usuario_id=user_id
        ).first()
        user_permission.fk_perfil_id = profile.id

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
