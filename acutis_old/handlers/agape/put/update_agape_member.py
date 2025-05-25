from http import HTTPStatus
from flask import request as flask_request
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.membro_agape import MembroAgape
from models.schemas.agape.put.update_agape_member import (
    UpdateAgapeMemberFormData,
)
from services.file_service import FileService
from utils.functions import get_current_time, is_valid_email, is_valid_name
from utils.regex import format_string
from utils.validator import cpf_cnpj_validator


class UpdateAgapeMember:
    def __init__(
        self, database: SQLAlchemy, file_service: FileService
    ) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self, fk_membro_agape_id: int):
        membro = UpdateAgapeMemberFormData(
            responsavel=flask_request.form['responsavel'],
            nome=flask_request.form['nome'],
            email=flask_request.form.get('email'),
            telefone=flask_request.form.get('telefone'),
            cpf=flask_request.form.get('cpf'),
            data_nascimento=flask_request.form['data_nascimento'],
            funcao_familiar=flask_request.form['funcao_familiar'],
            escolaridade=flask_request.form['escolaridade'],
            ocupacao=flask_request.form['ocupacao'],
            renda=flask_request.form.get('renda'),
            beneficiario_assistencial=flask_request.form['beneficiario_assistencial'],
            foto_documento=flask_request.files.get('foto_documento'),
        )
        try:
            db_membro = self.__get_agape_member_data(fk_membro_agape_id)
            self.__validate_data(membro, db_membro)
            self.__update_member(membro, db_membro)
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {"msg": "Membro atualizado com sucesso."}, HTTPStatus.OK

    def __get_agape_member_data(self, fk_membro_agape_id: int) -> MembroAgape:
        db_membro: MembroAgape = self.__database.session.get(
            MembroAgape, fk_membro_agape_id
        )
        if not db_membro:
            raise NotFoundError("Membro não encontrado.")
        return db_membro

    def __validate_data(
        self, membro: MembroAgape, db_membro: MembroAgape
    ) -> None:
        if membro.responsavel and membro.cpf is None:
            raise BadRequestError(
                f"O CPF do responsável {membro.nome} é obrigatório."
            )

        if membro.cpf:
            membro.cpf = cpf_cnpj_validator(membro.cpf, document_type="cpf")
            database_membro = MembroAgape.query.filter_by(
                cpf=membro.cpf
            ).first()
            if database_membro and database_membro.id != db_membro.id:
                raise ConflictError(
                    f"Ja existe um membro com o CPF {membro.cpf} cadastrado."
                )

        if membro.email:
            membro.email = is_valid_email(
                membro.email,
                check_deliverability=True,
                check_valid_domain=False,
            )
            database_membro = MembroAgape.query.filter_by(
                email=membro.email
            ).first()
            if database_membro and database_membro.id != db_membro.id:
                raise ConflictError(
                    f"Ja existe um membro com o email {membro.email} cadastrado."
                )

        membro.nome = is_valid_name(membro.nome)

    def __update_member(
        self, membro: MembroAgape, db_membro: MembroAgape
    ) -> None:
        membro.telefone = format_string(membro.telefone, only_digits=True)

        db_membro.responsavel = membro.responsavel
        db_membro.nome = membro.nome
        db_membro.email = membro.email
        db_membro.telefone = membro.telefone
        db_membro.cpf = membro.cpf
        db_membro.data_nascimento = membro.data_nascimento
        db_membro.funcao_familiar = membro.funcao_familiar
        db_membro.escolaridade = membro.escolaridade
        db_membro.ocupacao = membro.ocupacao
        db_membro.renda = membro.renda
        db_membro.beneficiario_assistencial = membro.beneficiario_assistencial
        db_membro.atualizado_em = get_current_time()

        if membro.foto_documento:
            if db_membro.foto_documento:
                self.__file_service.delete_object(db_membro.foto_documento)
            db_membro.foto_documento = self.__file_service.upload_image(
                membro.foto_documento
            )

        self.__database.session.commit()
