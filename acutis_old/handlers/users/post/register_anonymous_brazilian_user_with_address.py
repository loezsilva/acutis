from http import HTTPStatus
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from handlers.users.post.interfaces.register_anonymous_user_interface import (
    RegisterAnonymousBrazilianUserWithAddressInterface,
)
from models.clifor import Clifor
from models.endereco import Endereco
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.schemas.users.post.register_brazilian_user_with_address import (
    RegisterBrazilianUserWithAddressRequest,
)
from models.usuario import Usuario
from templates.email_templates import (
    active_account_alistamento_email_template,
)
from utils.functions import get_current_time
from utils.send_email import send_email
from utils.token_email import generate_token


class RegisterAnonymousBrazilianUserWithAddress(
    RegisterAnonymousBrazilianUserWithAddressInterface
):
    def register(
        self,
        database=SQLAlchemy,
        clifor=Clifor,
        perfil=Perfil,
        origem_cadastro=Optional[int],
        request=RegisterBrazilianUserWithAddressRequest,
    ):
        db_usuario = self.__register_user_data(
            database, request.usuario, origem_cadastro
        )
        self.__register_clifor_data(clifor, db_usuario, request.usuario)
        self.__register_user_address_data(database, clifor, request.endereco)
        self.__register_user_permissions(database, db_usuario, perfil)
        self.__send_email_verification(db_usuario, request.usuario)
        self.__commit_changes(database)

        return {"msg": "Usuário cadastrado com sucesso."}, HTTPStatus.CREATED

    def __register_user_data(
        self,
        database: SQLAlchemy,
        usuario: Usuario,
        origem_cadastro: Optional[int],
    ) -> Usuario:

        db_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            password=usuario.password,
            country="brasil",
            origem_cadastro=origem_cadastro,
            campanha_origem=usuario.campanha_origem,
            data_inicio=get_current_time(),
            obriga_atualizar_cadastro=False,
        )

        database.session.add(db_usuario)
        database.session.flush()

        return db_usuario

    def __register_clifor_data(
        self, db_clifor: Clifor, db_usuario: Usuario, usuario: Usuario
    ) -> None:

        db_clifor.fk_usuario_id = db_usuario.id
        db_clifor.nome = usuario.nome
        db_clifor.cpf_cnpj = usuario.cpf
        db_clifor.email = usuario.email
        db_clifor.data_nascimento = usuario.data_nascimento
        db_clifor.usuario_criacao = db_usuario.id
        db_clifor.sexo = usuario.sexo

    def __register_user_address_data(
        self, database: SQLAlchemy, db_clifor: Clifor, endereco: Endereco
    ) -> None:
        address = Endereco(
            fk_clifor_id=db_clifor.id,
            rua=endereco.rua,
            numero=endereco.numero,
            complemento=endereco.complemento,
            bairro=endereco.bairro,
            cidade=endereco.cidade,
            estado=endereco.estado,
            cep=endereco.cep,
            pais_origem="brasil",
            obriga_atualizar_endereco=False,
        )
        database.session.add(address)

    def __register_user_permissions(
        self, database: SQLAlchemy, db_usuario: Usuario, db_perfil: Perfil
    ) -> None:
        user_permission = PermissaoUsuario(
            fk_usuario_id=db_usuario.id,
            fk_perfil_id=db_perfil.id,
            usuario_criacao=db_usuario.id,
        )
        database.session.add(user_permission)

    def __send_email_verification(
        self,
        db_usuario: Usuario,
        usuario: Usuario,
    ) -> None:

        data_to_generate_token_esm = {
            "email": usuario.email,
            "telefone": usuario.telefone,
            "nome": usuario.nome,
            "usuario_id": db_usuario.id,
            "landing_id": 18,
            "tipo_cadastro": "alistamento",
        }

        token = generate_token(
            obj=data_to_generate_token_esm,
            salt="active_account_confirmation",
        )

        html = active_account_alistamento_email_template(usuario.nome, token)
        send_email("HeSed - Verificação de Email", usuario.email, html, 1)

    def __commit_changes(self, database: SQLAlchemy) -> None:
        database.session.commit()
