from http import HTTPStatus
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request
from werkzeug.datastructures import FileStorage

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from handlers.users.post.interfaces.register_anonymous_user_interface import (
    RegisterAnonymousUserFullInterface,
)
from handlers.users.post.interfaces.register_deleted_user_interface import (
    RegisterDeletedUserFullInterface,
)
from handlers.users.utils.functions import (
    choose_template_active_account_to_send,
)
from models.campanha import Campanha
from models.clifor import Clifor
from models.endereco import Endereco
from models.landpage_usuarios import LandpageUsers
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from models.schemas.users.post.register_user_full import (
    RedirectPagesEnum,
    RegisterUserFullFormData,
)
from models.users_imports import UsersImports
from models.usuario import Usuario
from services.file_service import FileService
from services.send_data_to_app_acutis import SendDataToAppAcutis
from utils.functions import (
    get_current_time,
    is_valid_birthdate,
    is_valid_email,
    is_valid_name,
)
from utils.regex import format_string, validate_password
from utils.validator import cpf_cnpj_validator


class RegisterUserFull:
    def __init__(
        self,
        database: SQLAlchemy,
        file_service: FileService,
        register_deleted_user: RegisterDeletedUserFullInterface,
        register_anonymous_user: RegisterAnonymousUserFullInterface,
    ) -> None:
        self.__database = database
        self.__file_service = file_service
        self.__register_deleted_user = register_deleted_user
        self.__register_anonymous_user = register_anonymous_user

    def execute(self):
        request = RegisterUserFullFormData(
            image=flask_request.files.get("image"),
            pais=flask_request.form.get("pais", "brasil"),
            pagina_redirecionamento=flask_request.form.get(
                "pagina_redirecionamento", RedirectPagesEnum.PRINCIPAL
            ),
            usuario=flask_request.form["usuario"],
            endereco=flask_request.form["endereco"],
        )
        self.__validate_request_data(request)
        registro = self.__get_user_type_registering(
            request.usuario.numero_documento, request.usuario.tipo_documento
        )
        if registro[0] == "usuario_deletado":
            return self.__register_deleted_user.register(
                database=self.__database,
                file_service=self.__file_service,
                usuario=registro[2],
                clifor=registro[1],
                request=request,
            )
        self.__validate_telefone(request.usuario.telefone)
        self.__validate_email_in_use(request.usuario.email)
        perfil = self.__get_profile()
        origem_cadastro = self.__get_user_is_import(request.usuario.email)

        if registro[0] == "usuario_anonimo":
            return self.__register_anonymous_user.register(
                database=self.__database,
                file_service=self.__file_service,
                clifor=registro[1],
                perfil=perfil,
                request=request,
                origem_cadastro=origem_cadastro,
            )

        usuario = self.__register_user_data(
            usuario=request.usuario,
            pais=request.pais,
            origem_cadastro=origem_cadastro,
            avatar=request.image,
        )
        clifor = self.__register_clifor_data(usuario, request.usuario)
        self.__register_user_address_data(
            clifor, request.endereco, request.pais
        )
        self.__register_user_permissions(usuario, perfil)
        choose_template_active_account_to_send(
            db_usuario=usuario,
            usuario=request.usuario,
            pais=request.pais,
            pagina_redirecionamento=request.pagina_redirecionamento,
        )
        self.__register_landpage_user(request.usuario.campanha_origem, clifor)
        
        if request.usuario.campanha_origem == 43:
            # envia dados do usuário para o app acutis quando cadastro realizado na campanha 43
            payload = {
                "email": clifor.email,
                "cpf": clifor.cpf_cnpj,
                "patent": "membro",
                "name": clifor.nome
            }
                        
            register_general_in_app_acutis = SendDataToAppAcutis(payload)
            register_general_in_app_acutis.execute()

        return {"msg": "Usuário cadastrado com sucesso."}, HTTPStatus.CREATED

    def __validate_request_data(
        self, request: RegisterUserFullFormData
    ) -> None:
        if request.pais.lower() == "brasil":
            campos_endereco = [
                request.endereco.cep,
                request.endereco.rua,
                request.endereco.numero,
                request.endereco.bairro,
                request.endereco.estado,
                request.endereco.cidade,
            ]
            preenchimento_completo_endereco_brasileiro = all(
                campo is not None for campo in campos_endereco
            )
            if not preenchimento_completo_endereco_brasileiro:
                raise BadRequestError(
                    "O preenchimento completo do endereço é obrigatório."
                )

        elif (
            request.pais.lower() != "brasil"
            and request.endereco.detalhe_estrangeiro is None
        ):
            raise BadRequestError(
                "O preenchimento completo do endereço de estrangeiro é obrigatório."
            )

        request.endereco.cep = format_string(
            request.endereco.cep, only_digits=True
        )
        request.usuario.numero_documento = cpf_cnpj_validator(
            request.usuario.numero_documento, request.usuario.tipo_documento
        )
        request.usuario.nome = is_valid_name(request.usuario.nome.strip())
        request.usuario.nome_social = is_valid_name(
            request.usuario.nome_social
        )
        request.usuario.data_nascimento = is_valid_birthdate(
            request.usuario.data_nascimento
        )
        request.usuario.email = is_valid_email(
            request.usuario.email.strip(),
            check_deliverability=True,
            check_valid_domain=False,
        )
        request.usuario.password = validate_password(
            request.usuario.password.get_secret_value()
        )
        request.usuario.telefone = format_string(
            request.usuario.telefone.strip(), only_digits=True
        )

    def __get_user_type_registering(
        self, numero_documento: str, tipo_documento: Optional[str] = "cpf"
    ):
        clifor = Clifor.query.filter_by(cpf_cnpj=numero_documento).first()
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
        email_already_registered = Usuario.query.filter_by(email=email).first()
        if email_already_registered:
            raise ConflictError("Email já cadastrado.")

    def __get_profile(self) -> Perfil:
        profile = Perfil.query.filter(Perfil.nome.ilike("Benfeitor")).first()
        if profile is None:
            raise NotFoundError("Perfil não encontrado.")
        return profile

    def __get_user_is_import(self, email: str) -> Optional[int]:
        user_import: UsersImports = UsersImports.query.filter_by(
            email=email
        ).first()
        return user_import.origem_cadastro if user_import else None

    def __register_user_data(
        self,
        usuario: Usuario,
        pais: Optional[str],
        origem_cadastro: Optional[int],
        avatar: Optional[FileStorage],
    ) -> Usuario:
        db_usuario = Usuario(
            nome=usuario.nome,
            nome_social=usuario.nome_social,
            avatar=(
                self.__file_service.upload_image(avatar) if avatar else None
            ),
            email=usuario.email,
            password=usuario.password,
            country=pais,
            origem_cadastro=origem_cadastro,
            campanha_origem=usuario.campanha_origem,
            data_inicio=get_current_time(),
            obriga_atualizar_cadastro=True,
        )

        self.__database.session.add(db_usuario)
        self.__database.session.flush()

        return db_usuario

    def __register_clifor_data(
        self,
        db_usuario: Usuario,
        usuario: Clifor,
    ) -> Clifor:

        self.__validate_telefone(usuario.telefone)

        clifor = Clifor(
            fk_usuario_id=db_usuario.id,
            nome=usuario.nome,
            cpf_cnpj=usuario.numero_documento,
            email=usuario.email,
            data_nascimento=usuario.data_nascimento,
            usuario_criacao=db_usuario.id,
            telefone1=usuario.telefone,
            sexo=usuario.sexo,
        )
        self.__database.session.add(clifor)
        self.__database.session.flush()

        return clifor

    def __register_user_address_data(
        self, db_clifor: Clifor, endereco: Endereco, pais: Optional[str]
    ) -> None:
        db_endereco = Endereco(
            fk_clifor_id=db_clifor.id,
            rua=endereco.rua,
            numero=endereco.numero,
            complemento=endereco.complemento,
            ponto_referencia=endereco.ponto_referencia,
            bairro=endereco.bairro,
            cidade=endereco.cidade,
            estado=endereco.estado,
            cep=endereco.cep,
            detalhe_estrangeiro=endereco.detalhe_estrangeiro,
            pais_origem=pais,
            obriga_atualizar_endereco=True if not pais else False,
        )
        self.__database.session.add(db_endereco)

    def __register_user_permissions(
        self, db_usuario: Usuario, perfil: Perfil
    ) -> None:
        permissao_usuario = PermissaoUsuario(
            fk_usuario_id=db_usuario.id,
            fk_perfil_id=perfil.id,
            usuario_criacao=db_usuario.id,
        )
        self.__database.session.add(permissao_usuario)

    def __register_landpage_user(
        self, campanha_origem: Optional[int], clifor: Clifor
    ) -> None:
        if campanha_origem:
            campanha = self.__database.session.get(Campanha, campanha_origem)
            if campanha:
                landpage = campanha.landpage.first()
                if landpage:
                    landpage_user = LandpageUsers(
                        user_id=clifor.fk_usuario_id,
                        landpage_id=landpage.id,
                        campaign_id=campanha.id,
                        clifor_id=clifor.id,
                    )
                    self.__database.session.add(landpage_user)
        self.__database.session.commit()


    def __validate_telefone(self, telefone):
        telefone_formatado = format_string(
            telefone.strip(), only_digits=True
        )
        telefone_cadastrado = Clifor.query.filter_by(telefone1=telefone_formatado).first()
        if telefone_cadastrado is not None:
            raise ConflictError("Telefone já cadastrado")
        return telefone_formatado