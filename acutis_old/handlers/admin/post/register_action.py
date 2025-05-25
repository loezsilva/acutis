import json
from typing import Optional, Tuple
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request
from werkzeug.datastructures import FileStorage


from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_conflict import ConflictError
from models.actions_leads import ActionsLeads
from models.schemas.admin.post.register_action import RegisterActionRequest
from services.file_service import FileService
from utils.functions import get_current_time


class RegisterAction:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self):
        request = RegisterActionRequest.parse_obj(
            json.loads(flask_request.form.get("data"))
        )
        photo_background: Optional[FileStorage] = flask_request.files.get("background")
        photo_banner = self.__validate_data(
            request.preenchimento_foto, request.label_foto
        )
        self.__check_if_action_already_exists(request.nome)

        banner_filename, background_filename = self.__save_action_photos(
            photo_background, photo_banner
        )
        self.__register_action(request, banner_filename, background_filename)
        self.__commit_changes()

        return {"msg": "Ação cadastrada com sucesso!"}, 201

    def __validate_data(
        self, preenchimento_foto: bool, label_foto: Optional[str]
    ) -> FileStorage:
        if preenchimento_foto == True and label_foto is None:
            raise BadRequestError("O preenchimento do campo label foto é obrigatório.")

        photo_banner: FileStorage = flask_request.files.get("banner")
        if photo_banner is None:
            raise BadRequestError("O envio da foto do banner é obrigatório.")

        return photo_banner

    def __check_if_action_already_exists(self, nome: str) -> None:
        action = ActionsLeads.query.filter_by(nome=nome).first()
        if action:
            raise ConflictError("Ação já cadastrada.")

    def __save_action_photos(
        self, photo_background: Optional[FileStorage], photo_banner: FileStorage
    ) -> Tuple[str, Optional[str]]:
        banner_filename = self.__file_service.upload_image(photo_banner)
        if photo_background:
            background_filename = self.__file_service.upload_image(photo_background)
            return banner_filename, background_filename

        return banner_filename, None

    def __register_action(
        self,
        request: RegisterActionRequest,
        banner_filename: str,
        background_filename: Optional[str],
    ) -> None:
        new_action = ActionsLeads(
            nome=request.nome,
            titulo=request.titulo,
            descricao=request.descricao,
            background=background_filename,
            banner=banner_filename,
            status=request.status,
            sorteio=False,
            preenchimento_foto=request.preenchimento_foto,
            label_foto=request.label_foto,
            created_at=get_current_time(),
            cadastrado_por=current_user["id"],
        )
        self.__database.session.add(new_action)

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
