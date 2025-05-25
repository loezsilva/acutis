from http import HTTPStatus
from typing import List
from flask import request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.datastructures import FileStorage

from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.doacao_agape import DoacaoAgape
from models.agape.familia_agape import FamiliaAgape
from models.agape.recibo_agape import ReciboAgape
from services.file_service import FileService


class RegisterAgapeDonationReceipts:
    def __init__(self, database: SQLAlchemy, file_service: FileService):
        self.__database = database
        self.__file_service = file_service

    def execute(self, fk_doacao_agape_id: int):
        recibos = request.files.getlist("recibos")
        try:
            self.__validate_receipts_files(recibos)
            doacao_agape = self.__get_agape_donation(fk_doacao_agape_id)
            familia = self.__get_family_data(doacao_agape.fk_familia_agape_id)
            self.__register_receipts(recibos, doacao_agape, familia)
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {
            "msg": "Recibos da doação registrados com sucesso."
        }, HTTPStatus.CREATED

    def __validate_receipts_files(self, recibos: List[FileStorage]) -> None:
        for recibo in recibos:
            if recibo.filename == "":
                raise BadRequestError("Nome do arquivo inválido.")

            extension = recibo.filename.rsplit(".", 1)[1].lower()

            allowed_extensions = {"png", "jpg", "jpeg"}
            if extension not in allowed_extensions:
                raise BadRequestError("Extensão do arquivo não permitida.")

    def __get_agape_donation(self, fk_doacao_agape_id: int) -> DoacaoAgape:
        doacao_agape = self.__database.session.get(
            DoacaoAgape, fk_doacao_agape_id
        )
        if doacao_agape is None:
            raise NotFoundError("Doação ágape não encontrada.")
        return doacao_agape

    def __get_family_data(self, fk_familia_agape_id: int) -> None:
        familia: FamiliaAgape = self.__database.session.get(
            FamiliaAgape, fk_familia_agape_id
        )
        return familia

    def __register_receipts(
        self,
        recibos: List[FileStorage],
        doacao_agape: DoacaoAgape,
        familia: FamiliaAgape,
    ) -> None:
        for index, recibo in enumerate(recibos, start=1):
            filename = f"recibo_{familia.nome_familia}_{doacao_agape.created_at.strftime('%d-%m-%Y_%H-%M-%S')}_{index}.{recibo.filename.rsplit('.', 1)[1].lower()}"

            filename = self.__file_service.upload_image(
                file=recibo, filename=filename
            )
            recibo_agape = ReciboAgape(
                fk_doacao_agape_id=doacao_agape.id, recibo=filename
            )
            self.__database.session.add(recibo_agape)
        self.__database.session.commit()
