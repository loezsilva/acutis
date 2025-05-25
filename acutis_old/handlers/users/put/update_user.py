from datetime import date
import json
from typing import Optional
from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_not_found import NotFoundError
from models.clifor import Clifor
from models.endereco import Endereco
from models.schemas.users.put.update_user import (
    UpdateUserRequest,
    UserAddressUpdateSchema,
)
from models.usuario import Usuario
from services.file_service import FileService
from utils.functions import get_current_time, is_valid_birthdate, is_valid_name
from utils.regex import format_string


class UpdateUser:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        avatar, user_request = self.__validate_data()

        user_update_request = UpdateUserRequest.parse_obj(user_request)
        nome = is_valid_name(user_update_request.usuario.nome.strip())
        nome_social = is_valid_name(user_update_request.usuario.nome_social)
        sexo = user_update_request.usuario.sexo
        data_nascimento = is_valid_birthdate(
            user_update_request.usuario.data_nascimento
        )
        telefone = format_string(
            user_update_request.usuario.telefone.strip(), only_digits=True
        )
        user = self.__get_user_data(current_user["id"])
        self.__validate_if_user_sent_address(user.country, user_update_request.endereco)

        clifor = self.__get_clifor_data(current_user["fk_clifor_id"])
        address = self.__get_user_address_data(clifor.id)

        self.__update_user_data(
            nome=nome,
            nome_social=nome_social,
            data_nascimento=data_nascimento,
            telefone=telefone,
            avatar=avatar,
            sexo=sexo,
            user=user,
            clifor=clifor,
        )
        self.__update_user_address(address, user_update_request.endereco)
        self.__commit_changes()

        return {"msg": "Usuário atualizado com sucesso."}, 200

    def __validate_data(self) -> tuple:
        avatar: FileStorage = request.files.get("image")

        user_request = json.loads(request.form.get("data"))
        if user_request is None:
            raise BadRequestError("O envio dos dados são obrigatórios.")

        return avatar, user_request

    def __get_user_data(self, user_id: int) -> Usuario:
        user: Usuario = Usuario.query.filter_by(id=user_id, deleted_at=None).first()
        if user is None:
            raise NotFoundError("Usuário não encontrado.")

        return user

    def __get_clifor_data(self, clifor_id: int) -> Clifor:
        clifor: Clifor = self.__database.session.get(Clifor, clifor_id)
        if clifor is None:
            raise NotFoundError("Cliente não encontrado.")

        return clifor

    def __get_user_address_data(self, clifor_id: int) -> Endereco:
        address: Endereco = Endereco.query.filter_by(fk_clifor_id=clifor_id).first()
        if address is None:
            raise NotFoundError("Endereço do benfeitor não encontrado.")
        return address

    def __save_avatar_image(self, avatar: FileStorage) -> str:
        filename = self.__file_service.upload_image(avatar)
        return filename

    def __update_user_data(
        self,
        nome: str,
        nome_social: Optional[str],
        data_nascimento: date,
        telefone: str,
        avatar: Optional[FileStorage],
        sexo: str,
        user: Usuario,
        clifor: Clifor,
    ) -> None:
        if avatar:
            filename = self.__save_avatar_image(avatar)
            user.avatar = filename

        user.nome = nome
        user.nome_social = nome_social
        user.data_alteracao = get_current_time()
        user.usuario_alteracao = user.id
        user.obriga_atualizar_cadastro = False

        clifor.nome = nome
        clifor.data_nascimento = data_nascimento
        clifor.data_alteracao = get_current_time()
        clifor.usuario_alteracao = user.id
        clifor.sexo = sexo

    def __validate_if_user_sent_address(
        self, country: str, address_request: UserAddressUpdateSchema
    ) -> None:
        sent_address = (
            address_request.cep
            and address_request.rua
            and address_request.bairro
            and address_request.estado
            and address_request.cidade
        )
        if country == "brasil" and not sent_address:
            raise BadRequestError("O preenchimento do endereço é obrigatório.")

        if country != "brasil" and not address_request.detalhe_estrangeiro:
            raise BadRequestError(
                "O preenchimento do campo detalhe estrangeiro é obrigatório."
            )

    def __update_user_address(
        self, address: Endereco, address_request: UserAddressUpdateSchema
    ) -> None:
        address.cep = address_request.cep
        address.rua = address_request.rua
        address.numero = address_request.numero
        address.complemento = address_request.complemento
        address.bairro = address_request.bairro
        address.estado = address_request.estado
        address.cidade = address_request.cidade
        address.detalhe_estrangeiro = address_request.detalhe_estrangeiro
        address.obriga_atualizar_endereco = False
        address.ultima_atualizacao_endereco = get_current_time().date()
        address.usuario_alteracao = current_user["id"]
        address.data_alteracao = get_current_time()

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
