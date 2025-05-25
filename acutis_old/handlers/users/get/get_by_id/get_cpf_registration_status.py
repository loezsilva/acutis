from typing import Dict
from flask import request
from flask_sqlalchemy import SQLAlchemy

from models.clifor import Clifor
from models.endereco import Endereco
from models.schemas.users.get.get_cpf_registration_status import (
    GetCpfRegistrationStatusQuery,
)
from models.usuario import Usuario
from utils.validator import cpf_cnpj_validator


class GetCpfRegistrationStatus:
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def execute(self):
        query = GetCpfRegistrationStatusQuery.parse_obj(request.args)
        numero_documento = cpf_cnpj_validator(
            query.numero_documento, query.tipo_documento
        )
        user = self.__get_user_by_cpf(numero_documento)
        response = self.__prepare_response(user)
        return response, 200

    def __get_user_by_cpf(self, cpf: str):
        user = (
            self.__database.session.query(
                Usuario.nome,
                Usuario.nome_social,
                Usuario.obriga_atualizar_cadastro,
                Endereco.obriga_atualizar_endereco,
            )
            .select_from(Usuario)
            .join(Clifor, Usuario.id == Clifor.fk_usuario_id)
            .join(Endereco, Clifor.id == Endereco.fk_clifor_id)
            .filter(Clifor.cpf_cnpj == cpf)
        )

        user = user.first()

        return user

    def __prepare_response(self, user: Usuario) -> Dict:
        response = {}
        if user is None:
            response["possui_conta"] = False
            response["atualizar_conta"] = False
        else:
            response["possui_conta"] = True
            response["atualizar_conta"] = (
                user.obriga_atualizar_cadastro
                or user.obriga_atualizar_endereco
            )
        return response
