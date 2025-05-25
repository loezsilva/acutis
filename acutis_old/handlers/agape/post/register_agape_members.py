from http import HTTPStatus
from typing import List
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.familia_agape import FamiliaAgape
from models.agape.membro_agape import MembroAgape
from models.schemas.agape.post.register_agape_members import (
    AgapeMemberSchema,
    RegisterAgapeMembersRequest,
)
from services.file_service_interface import FileServiceInterface
from utils.functions import decodificar_base64_para_arquivo, is_valid_email, is_valid_name
from utils.regex import format_string
from utils.validator import cpf_cnpj_validator


class RegisterAgapeMembers:
    def __init__(self, 
        database: SQLAlchemy, 
        file_service: FileServiceInterface
    ) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self, fk_familia_agape_id: int):
        request = RegisterAgapeMembersRequest.parse_obj(flask_request.json)
        try:
            familia = self.__get_agape_family_data(fk_familia_agape_id)
            self.__register_family(
                request.membros, familia,
            )
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {"msg": "Membros cadastrados com sucesso."}, HTTPStatus.CREATED

    def __get_agape_family_data(
        self, fk_familia_agape_id: int
    ) -> FamiliaAgape:
        familia: FamiliaAgape = self.__database.session.get(
            FamiliaAgape, fk_familia_agape_id
        )
        if familia is None or familia.deleted_at is not None:
            raise NotFoundError("Família não encontrada.")
        return familia

    def __register_family(
        self, 
        membros: List[AgapeMemberSchema], 
        familia: FamiliaAgape,
    ):
        for membro in membros:
            if membro.responsavel and membro.cpf is None:
                raise BadRequestError(
                    f"O CPF do responsável {membro.nome} é obrigatório."
                )

            if membro.cpf:
                membro.cpf = cpf_cnpj_validator(
                    membro.cpf, document_type="cpf"
                )
                db_membro = MembroAgape.query.filter_by(cpf=membro.cpf).first()
                if db_membro:
                    raise ConflictError(
                        f"Ja existe um membro com o CPF {membro.cpf} cadastrado."
                    )

            if membro.email:
                membro.email = is_valid_email(
                    membro.email,
                    check_deliverability=True,
                    check_valid_domain=False,
                )
                db_membro = MembroAgape.query.filter_by(
                    email=membro.email
                ).first()
                if db_membro:
                    raise ConflictError(
                        f"Já existe um membro com o email {membro.email} cadastrado."
                    )

            membro.nome = is_valid_name(membro.nome)
            membro.telefone = format_string(membro.telefone, only_digits=True)

            membro_agape = MembroAgape(
                fk_familia_agape_id=familia.id,
                responsavel=membro.responsavel,
                nome=membro.nome,
                email=membro.email,
                telefone=membro.telefone,
                cpf=membro.cpf,
                data_nascimento=membro.data_nascimento,
                funcao_familiar=membro.funcao_familiar,
                escolaridade=membro.escolaridade,
                ocupacao=membro.ocupacao,
                renda=membro.renda,
                beneficiario_assistencial=membro.beneficiario_assistencial,
                foto_documento=(
                    self.__file_service.upload_image(
                        decodificar_base64_para_arquivo(
                            membro.foto_documento
                        )
                    ) if membro.foto_documento else None
                )
            )
            self.__database.session.add(membro_agape)
        self.__database.session.commit()
