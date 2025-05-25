from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario

from models.schemas.admin.get.get_by_id.get_user_by_id import (
    GetUserByIdResponse,
)
from models.usuario import Usuario
from services.file_service import FileService


class GetUserById:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self, fk_usuario_id: int):
        user = self.__get_user_by_id(fk_usuario_id)
        response = self.__prepare_response(user)

        return response, 200

    def __get_user_by_id(self, fk_usuario_id: int) -> Usuario:
        user_query = (
            self.__database.session.query(
                Usuario.id,
                Usuario.nome,
                Usuario.nome_social,
                Usuario.email,
                Usuario.country.label("pais"),
                Usuario.status,
                Usuario.origem_cadastro,
                func.format(Usuario.data_criacao, "dd/MM/yyyy").label("data_cadastro"),
                func.format(Usuario.data_ultimo_acesso, "dd/MM/yyyy").label(
                    "ultimo_acesso"
                ),
                Usuario.avatar,
                Clifor.cpf_cnpj.label("numero_documento"),
                Clifor.telefone1.label("telefone"),
                Perfil.nome.label("perfil"),
            )
            .select_from(Usuario)
            .join(Clifor, Usuario.id == Clifor.fk_usuario_id)
            .join(PermissaoUsuario, Usuario.id == PermissaoUsuario.fk_usuario_id)
            .join(Perfil, Perfil.id == PermissaoUsuario.fk_perfil_id)
            .filter(Usuario.id == fk_usuario_id, Usuario.deleted_at.is_(None))
        )

        user_data = user_query.first()

        if user_data is None:
            raise NotFoundError("Usuário não encontrado.")

        return user_data

    def __prepare_response(self, user: Usuario) -> dict:
        response = GetUserByIdResponse(
            id=user.id,
            nome=user.nome,
            nome_social=user.nome_social,
            email=user.email,
            pais=user.pais,
            status=user.status,
            origem_cadastro=user.origem_cadastro,
            data_cadastro=user.data_cadastro,
            ultimo_acesso=user.ultimo_acesso,
            avatar=(
                self.__file_service.get_public_url(user.avatar) if user.avatar else None
            ),
            numero_documento=user.numero_documento,
            telefone=user.telefone,
            perfil=user.perfil,
        ).dict()

        return response
