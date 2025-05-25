from http import HTTPStatus
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage

from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
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
    RegisterUserFullFormData,
)
from models.usuario import Usuario
from services.file_service import FileService
from services.send_data_to_app_acutis import SendDataToAppAcutis
from utils.functions import (
    get_current_time,
)
from utils.regex import format_string


class RegisterDeletedUserFull(RegisterDeletedUserFullInterface):
    def register(
        self,
        database: SQLAlchemy,
        file_service: FileService,
        usuario=Usuario,
        clifor=Clifor,
        request=RegisterUserFullFormData,
    ):  
        self.__validate_telefone(request.usuario.telefone1)
        self.__validate_email_in_use(request.usuario.email, usuario)
        self.__reset_user_address(clifor, request.endereco, request.pais)
        self.__register_user_deleted(
            file_service,
            usuario,
            clifor,
            request.usuario,
            request.pais,
            request.image,
        )
        self.__register_user_permissions(usuario)
        choose_template_active_account_to_send(
            db_usuario=usuario,
            usuario=request.usuario,
            pais=request.pais,
            pagina_redirecionamento=request.pagina_redirecionamento,
        )
        self.__register_landpage_user(
            database, request.usuario.campanha_origem, clifor
        )
        
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

    def __validate_email_in_use(self, email: str, db_usuario: Usuario) -> None:
        valid_email = Usuario.query.filter_by(email=email).first()
        if valid_email and valid_email.id != db_usuario.id:
            raise ConflictError("Email já cadastrado.")

    def __reset_user_address(
        self, clifor: Clifor, endereco: Endereco, pais: Optional[str]
    ) -> None:
        db_endereco: Endereco = Endereco.query.filter_by(
            fk_clifor_id=clifor.id
        ).first()

        db_endereco.rua = endereco.rua
        db_endereco.numero = endereco.numero
        db_endereco.complemento = endereco.complemento
        db_endereco.ponto_referencia = endereco.ponto_referencia
        db_endereco.bairro = endereco.bairro
        db_endereco.cidade = endereco.cidade
        db_endereco.estado = endereco.estado
        db_endereco.cep = endereco.cep
        db_endereco.obriga_atualizar_endereco = True if not pais else False
        db_endereco.detalhe_estrangeiro = endereco.detalhe_estrangeiro
        db_endereco.pais_origem = pais

    def __register_user_deleted(
        self,
        file_service: FileService,
        db_usuario: Usuario,
        db_clifor: Clifor,
        usuario: Usuario | Clifor,
        pais: Optional[str],
        avatar: Optional[FileStorage],
    ) -> None:

        db_usuario.country = pais
        db_usuario.nome = usuario.nome
        db_usuario.nome_social = usuario.nome_social
        db_usuario.email = usuario.email
        db_usuario.password = usuario.password
        db_usuario.avatar = (
            file_service.upload_image(avatar) if avatar else None
        )
        db_usuario.status = False
        db_usuario.deleted_at = None
        db_usuario.data_inicio = get_current_time()
        db_usuario.obriga_atualizar_cadastro = True
        db_usuario.campanha_origem = usuario.campanha_origem

        db_clifor.nome = usuario.nome
        db_clifor.email = usuario.email
        db_clifor.cpf_cnpj = usuario.numero_documento
        db_clifor.data_nascimento = usuario.data_nascimento
        db_clifor.sexo = usuario.sexo

    def __register_user_permissions(self, db_usuario: Usuario) -> None:
        perfil = Perfil.query.filter(Perfil.nome.ilike("Benfeitor")).first()
        if perfil is None:
            raise NotFoundError("Perfil não encontrado.")

        permissao_usuario = PermissaoUsuario.query.filter_by(
            fk_usuario_id=db_usuario.id
        ).first()
        permissao_usuario.fk_perfil_id = perfil.id

    def __register_landpage_user(
        self,
        database: SQLAlchemy,
        campanha_origem: Optional[int],
        clifor: Clifor,
    ) -> None:
        if campanha_origem:
            campanha = database.session.get(Campanha, campanha_origem)
            if campanha:
                landpage = campanha.landpage.first()
                if landpage:
                    landpage_user = LandpageUsers(
                        user_id=clifor.fk_usuario_id,
                        landpage_id=landpage.id,
                        campaign_id=campanha.id,
                        clifor_id=clifor.id,
                    )
                    database.session.add(landpage_user)
        database.session.commit()
        
    def __validate_telefone(self, telefone):
        telefone_formatado = format_string(
            telefone.strip(), only_digits=True
        )
        telefone_cadastrado = Clifor.query.filter_by(telefone1=telefone_formatado).first()
        if telefone_cadastrado is not None:
            raise ConflictError("Telefone já cadastrado")
        return telefone_formatado
