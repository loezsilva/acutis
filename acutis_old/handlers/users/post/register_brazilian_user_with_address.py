from http import HTTPStatus
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from handlers.users.post.interfaces.register_anonymous_user_interface import (
    RegisterAnonymousBrazilianUserWithAddressInterface,
)
from handlers.users.post.interfaces.register_deleted_user_interface import (
    RegisterDeletedBrazilianUserWithAddressInterface,
)
from models.clifor import Clifor
from models.endereco import Endereco
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.schemas.users.post.register_brazilian_user_with_address import (
    RegisterBrazilianUserWithAddressRequest,
)
from models.users_imports import UsersImports
from models.usuario import Usuario
from templates.email_templates import (
    active_account_alistamento_email_template,
)
from utils.functions import get_current_time, is_valid_email
from utils.regex import format_string, validate_password
from utils.send_email import send_email
from utils.token_email import generate_token
from utils.validator import cpf_cnpj_validator


class RegisterBrazilianUserWithAddress:
    def __init__(
        self,
        database: SQLAlchemy,
        register_deleted_user: RegisterDeletedBrazilianUserWithAddressInterface,
        register_anonymous_user: RegisterAnonymousBrazilianUserWithAddressInterface,
    ) -> None:
        self.__database = database
        self.__register_deleted_user = register_deleted_user
        self.__register_anonymous_user = register_anonymous_user

    def execute(self):
        request = RegisterBrazilianUserWithAddressRequest.parse_obj(
            flask_request.json
        )
        try:
                        
            self.__validate_data(request)
            registro = self.__get_user_type_registering(request.usuario.cpf)
            if registro[0] == "usuario_deletado":
                return self.__register_deleted_user.register(
                    database=self.__database,
                    usuario=registro[2],
                    clifor=registro[1],
                    request=request,
                )

            self.__validate_email_in_use(request.usuario.email)
            db_perfil = self.__get_profile("Benfeitor")
            origem_cadastro = self.__get_user_is_import(request.usuario.email)

            if registro[0] == "usuario_anonimo":
                return self.__register_anonymous_user.register(
                    database=self.__database,
                    clifor=registro[1],
                    perfil=db_perfil,
                    origem_cadastro=origem_cadastro,
                    request=request,
                )

            db_usuario = self.__register_user_data(
                request.usuario, origem_cadastro
            )
            db_clifor = self.__register_clifor_data(
                db_usuario, request.usuario
            )
            self.__register_user_address_data(db_clifor, request.endereco)
            self.__register_user_permissions(db_usuario, db_perfil)
            self.__send_email_verification(db_usuario, request.usuario)
            self.__commit_changes(self.__database)

            return {
                "msg": "Usuário cadastrado com sucesso."
            }, HTTPStatus.CREATED

        except Exception as exception:
            self.__database.session.rollback()
            raise exception

    def __validate_data(
        self, request: RegisterBrazilianUserWithAddressRequest
    ) -> None:
        request.usuario.email = is_valid_email(
            request.usuario.email,
            check_deliverability=True,
            check_valid_domain=False,
        )
        request.usuario.cpf = cpf_cnpj_validator(request.usuario.cpf, "cpf")
        request.usuario.telefone = format_string(
            request.usuario.telefone, only_digits=True
        )
        request.usuario.password = validate_password(
            request.usuario.password.get_secret_value()
        )
        request.endereco.cep = format_string(
            request.endereco.cep, only_digits=True
        )

    def __get_user_type_registering(
        self, cpf: str, tipo_documento: Optional[str] = "cpf"
    ):
        clifor = Clifor.query.filter_by(cpf_cnpj=cpf).first()
        if clifor:
            if clifor.fk_usuario_id:
                usuario = self.__database.session.get(
                    Usuario, clifor.fk_usuario_id
                )
                if usuario.deleted_at is not None:
                    return ("usuario_deletado", clifor, usuario)

                raise ConflictError(
                    f"{format_string(tipo_documento.title(), lower=False)} já cadastrado."
                )

            return ("usuario_anonimo", clifor)
        return ("usuario_novo",)

    def __validate_email_in_use(self, email: str) -> None:
        email_ja_registrado = Clifor.query.filter_by(email=email).first()
        if email_ja_registrado:
            raise ConflictError("Email já cadastrado.")

    def __get_profile(self, nome_perfil: str) -> Perfil:
        perfil = Perfil.query.filter(Perfil.nome.ilike(nome_perfil)).first()
        if perfil is None:
            raise NotFoundError("Perfil não encontrado.")
        return perfil

    def __get_user_is_import(self, email: str) -> Optional[int]:
        user_import: UsersImports = UsersImports.query.filter_by(
            email=email
        ).first()
        return user_import.origem_cadastro if user_import else None

    def __register_user_data(
        self, usuario: Usuario, origem_cadastro: Optional[int]
    ) -> Usuario:

        db_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            password=usuario.password,
            country="brasil",
            campanha_origem=usuario.campanha_origem,
            origem_cadastro=origem_cadastro,
            data_inicio=get_current_time(),
            obriga_atualizar_cadastro=True,
        )

        self.__database.session.add(db_usuario)
        self.__database.session.flush()

        return db_usuario

    def __register_clifor_data(
        self,
        db_usuario: Usuario,
        usuario: Usuario,
    ) -> Clifor:

        usuario.telefone = self.__validate_telefone(
            usuario.telefone
        )

        db_clifor = Clifor(
            fk_usuario_id=db_usuario.id,
            nome=usuario.nome,
            cpf_cnpj=usuario.cpf,
            email=usuario.email,
            data_nascimento=usuario.data_nascimento,
            telefone1=usuario.telefone,
            sexo=usuario.sexo,
            usuario_criacao=db_usuario.id,
        )
        self.__database.session.add(db_clifor)
        self.__database.session.flush()

        return db_clifor

    def __register_user_address_data(
        self, db_clifor: Clifor, endereco: Endereco
    ) -> None:
        db_endereco = Endereco(
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
        self.__database.session.add(db_endereco)

    def __register_user_permissions(
        self, db_usuario: Usuario, db_perfil: Perfil
    ) -> None:
        permissao_usuario = PermissaoUsuario(
            fk_usuario_id=db_usuario.id,
            fk_perfil_id=db_perfil.id,
            usuario_criacao=db_usuario.id,
        )
        self.__database.session.add(permissao_usuario)

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
        
    def __validate_telefone(self, telefone):
        telefone_formatado = format_string(
            telefone.strip(), only_digits=True
        )
        telefone_cadastrado = Clifor.query.filter_by(telefone1=telefone_formatado).first()
        if telefone_cadastrado is not None:
            raise ConflictError("Telefone já cadastrado")
        return telefone_formatado
