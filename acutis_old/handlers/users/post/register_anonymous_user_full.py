from http import HTTPStatus
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage

from handlers.users.post.interfaces.register_anonymous_user_interface import (
    RegisterAnonymousUserFullInterface,
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


class RegisterAnonymousUserFull(RegisterAnonymousUserFullInterface):
    def register(
        self,
        database: SQLAlchemy,
        file_service: FileService,
        clifor: Clifor,
        perfil: Perfil,
        request: RegisterUserFullFormData,
        origem_cadastro: Optional[int],
    ):
        usuario = self.__register_user_data(
            database=database,
            file_service=file_service,
            usuario=request.usuario,
            pais=request.pais,
            origem_cadastro=origem_cadastro,
            avatar=request.image,
        )

        self.__register_clifor_data(clifor, usuario, request.usuario)
        self.__register_user_address_data(
            database=database,
            db_clifor=clifor,
            endereco=request.endereco,
            pais=request.pais,
        )
        self.__register_user_permissions(database, usuario, perfil)
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

    def __register_user_data(
        self,
        database: SQLAlchemy,
        file_service: FileService,
        usuario: Usuario,
        pais: Optional[str],
        origem_cadastro: Optional[int],
        avatar: Optional[FileStorage],
    ) -> Usuario:
        db_usuario = Usuario(
            nome=usuario.nome,
            nome_social=usuario.nome_social,
            avatar=file_service.upload_image(avatar) if avatar else None,
            email=usuario.email,
            password=usuario.password,
            country=pais,
            origem_cadastro=origem_cadastro,
            campanha_origem=usuario.campanha_origem,
            data_inicio=get_current_time(),
            obriga_atualizar_cadastro=True,
        )

        database.session.add(db_usuario)
        database.session.flush()

        return db_usuario

    def __register_clifor_data(
        self, db_clifor: Clifor, db_usuario: Usuario, usuario: Clifor
    ) -> None:
        db_clifor.fk_usuario_id = db_usuario.id
        db_clifor.nome = usuario.nome
        db_clifor.cpf_cnpj = usuario.numero_documento
        db_clifor.email = usuario.email
        db_clifor.data_nascimento = usuario.data_nascimento
        db_clifor.usuario_criacao = db_usuario.id
        db_clifor.sexo = usuario.sexo

    def __register_user_address_data(
        self,
        database: SQLAlchemy,
        db_clifor: Clifor,
        endereco: Endereco,
        pais: Optional[str],
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
        database.session.add(db_endereco)

    def __register_user_permissions(
        self, database: SQLAlchemy, db_usuario: Usuario, perfil: Perfil
    ) -> None:
        permissao_usuario = PermissaoUsuario(
            fk_usuario_id=db_usuario.id,
            fk_perfil_id=perfil.id,
            usuario_criacao=db_usuario.id,
        )
        database.session.add(permissao_usuario)

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
