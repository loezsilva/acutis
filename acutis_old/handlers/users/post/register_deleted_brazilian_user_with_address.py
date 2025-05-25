from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
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
from models.usuario import Usuario
from templates.email_templates import (
    active_account_alistamento_email_template,
)
from utils.functions import get_current_time
from utils.send_email import send_email
from utils.token_email import generate_token


class RegisterDeletedBrazilianUserWithAddress(
    RegisterDeletedBrazilianUserWithAddressInterface
):
    def register(
        self,
        database: SQLAlchemy,
        usuario=Usuario,
        clifor=Clifor,
        request=RegisterBrazilianUserWithAddressRequest,
    ):
        self.__validate_email_in_use(request.usuario.email, usuario)
        self.__reset_user_address(clifor, request.endereco)
        self.__register_deleted_brazilian_user(
            usuario, clifor, request.usuario
        )
        self.__register_user_permissions(usuario)
        self.__send_email_verification(usuario, request.usuario)
        self.__commit_changes(database)

        return {"msg": "Usuário cadastrado com sucesso."}, HTTPStatus.CREATED

    def __validate_email_in_use(self, email: str, usuario: Usuario) -> None:
        db_usuario = Usuario.query.filter_by(email=email).first()
        if db_usuario and db_usuario.id != usuario.id:
            raise ConflictError("Email já cadastrado.")

    def __reset_user_address(self, clifor: Clifor, endereco: Endereco) -> None:
        db_endereco = Endereco.query.filter_by(fk_clifor_id=clifor.id).first()

        db_endereco.rua = endereco.rua
        db_endereco.numero = endereco.numero
        db_endereco.complemento = endereco.complemento
        db_endereco.bairro = endereco.bairro
        db_endereco.cidade = endereco.cidade
        db_endereco.estado = endereco.estado
        db_endereco.cep = endereco.cep
        db_endereco.obriga_atualizar_endereco = False
        db_endereco.detalhe_estrangeiro = None
        db_endereco.pais_origem = "brasil"

    def __register_deleted_brazilian_user(
        self,
        db_usuario: Usuario,
        db_clifor: Clifor,
        usuario: Usuario,
    ) -> None:
        db_usuario.country = "brasil"
        db_usuario.nome = usuario.nome
        db_usuario.nome_social = None
        db_usuario.email = usuario.email
        db_usuario.password = usuario.password
        db_usuario.avatar = None
        db_usuario.status = False
        db_usuario.deleted_at = None
        db_usuario.data_inicio = get_current_time()
        db_usuario.obriga_atualizar_cadastro = False
        db_usuario.campanha_origem = usuario.campanha_origem

        db_clifor.nome = usuario.nome
        db_clifor.email = usuario.email
        db_clifor.cpf_cnpj = usuario.cpf
        db_clifor.data_nascimento = usuario.data_nascimento
        db_clifor.sexo = usuario.sexo

    def __register_user_permissions(self, usuario: Usuario) -> None:
        perfil = Perfil.query.filter(Perfil.nome.ilike("Benfeitor")).first()
        if perfil is None:
            raise NotFoundError("Perfil não encontrado.")

        permissao = PermissaoUsuario.query.filter_by(
            fk_usuario_id=usuario.id
        ).first()
        permissao.fk_perfil_id = perfil.id

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
