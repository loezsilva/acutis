from http import HTTPStatus
import json
from typing import Tuple
from flask import request
from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from exceptions.error_types.http_not_found import NotFoundError
from models.schemas.vocacional.post.registrar_ficha_vocacional_request import (
    RegistrarFichaVocacionalFormData,
    FormFichaVocacionalSchema,
)
from builder import db
from models.vocacional.ficha_vocacional import FichaVocacional
from models.vocacional.usuario_vocacional import UsuarioVocacional
from repositories.interfaces.vocacional.vocacional_repository_interface import (
    InterfaceVocacionalRepository,
)
from utils.functions import get_current_time


class RegistrarFichaVocacional:
    def __init__(
        self, s3_service, ficha_vocacional_repository: InterfaceVocacionalRepository
    ):
        self.__ficha_vocacional_repository = ficha_vocacional_repository
        self.__s3_service = s3_service

    def execute(self) -> Tuple[dict, HTTPStatus]:
        http_request = RegistrarFichaVocacionalFormData.parse_obj(request.form)

        ficha_data = json.loads(http_request.ficha_vocacional)
        ficha_validada = FormFichaVocacionalSchema.parse_obj(ficha_data)

        if "foto_vocacional" not in request.files:
            raise BadRequestError("Arquivo da foto vocacional não fornecido.")

        filename = f"foto_vocacional_{ficha_validada.fk_usuario_vocacional_id}_{get_current_time().strftime('%Y%m%d%H%M%S')}"
        file_foto_vocacional = request.files["foto_vocacional"]

        self.__s3_service.upload_image(file_foto_vocacional, filename)

        return self.__ficha_vocacional_repository.register_ficha_vocacional(
            ficha_validada, filename
        )
