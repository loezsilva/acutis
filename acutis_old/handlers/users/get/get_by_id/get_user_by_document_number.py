from http import HTTPStatus
from typing import Dict, Optional
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy
from models.clifor import Clifor
from models.endereco import Endereco
from models.generais import Generais
from models.usuario import Usuario
from models.schemas.users.get.get_user_by_document_number import (
    GetUserByDocumentNumberRequest,
    GetUserByDocumentNumberResponse,
)
from templates.email_templates import verify_become_general
from utils.functions import mask_email
from utils.send_email import send_email
from utils.token_email import generate_token
from utils.validator import cpf_cnpj_validator


class GetUserByDocumentNumber:
    def __init__(self, database: SQLAlchemy):
        self.__database = database

    def execute(self):
        request = GetUserByDocumentNumberRequest.parse_obj(flask_request.json)
        request.numero_documento = cpf_cnpj_validator(
            request.numero_documento, request.tipo_documento
        )
        clifor = self.__get_clifor_by_document_number(request.numero_documento)
        general = self.__get_general_by_document_number(
            request.numero_documento
        )
        response = self.__format_response(clifor, general)

        return response, HTTPStatus.OK

    def __get_clifor_by_document_number(
        self, numero_documento: str
    ) -> Optional[Clifor]:
        clifor: Clifor = (
            self.__database.session.query(
                Clifor.nome,
                Clifor.email,
                Clifor.telefone1,
                Clifor.fk_usuario_id,
                Endereco.pais_origem,
            )
            .join(Usuario, Clifor.fk_usuario_id == Usuario.id)
            .join(Endereco, Clifor.id == Endereco.fk_clifor_id)
            .filter(
                Clifor.cpf_cnpj == numero_documento,
                Usuario.deleted_at.is_(None),
            )
            .first()
        )

        return clifor

    def __get_general_by_document_number(
        self, numero_documento: str
    ) -> Optional[Generais]:
        general: Generais = (
            Generais.query.join(Usuario, Generais.fk_usuario_id == Usuario.id)
            .join(Clifor, Clifor.fk_usuario_id == Usuario.id)
            .filter(
                Clifor.cpf_cnpj == numero_documento,
                Usuario.deleted_at.is_(None),
                Generais.deleted_at.is_(None),
            )
            .first()
        )

        return general

    def __format_response(
        self,
        clifor: Optional[Clifor],
        general: Optional[Generais],
    ) -> Dict:

        # if clifor is not None and general is None:
        #     user_data_response = {
        #         "nome": clifor.nome,
        #         "email": clifor.email,
        #         "telefone": clifor.telefone1,
        #         "usuario_id": clifor.fk_usuario_id,
        #         "pais": clifor.pais_origem,
        #         "tipo_cadastro": "alistamento",
        #     }

        #     token = generate_token(
        #         user_data_response, salt="active_account_confirmation"
        #     )

        #     html = verify_become_general(token)
        #     send_email(
        #         assunto="HeSed - Deseja tornar-se General?",
        #         destinatario=clifor.email,
        #         conteudo=html,
        #         tipo=1,
        #     )

        response = GetUserByDocumentNumberResponse(
            usuario=True if clifor != None else False,
            general=True if general != None else False,
            email=mask_email(clifor.email) if clifor else None,
        ).dict()

        return response
