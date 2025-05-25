import json
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request
from werkzeug.datastructures import FileStorage


from exceptions.error_types.http_bad_request import BadRequestError
from exceptions.error_types.http_not_found import NotFoundError
from models.actions_leads import ActionsLeads
from models.schemas.admin.put.update_action import UpdateActionRequest
from services.file_service import FileService


class UpdateAction:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self, fk_acao_id: int):
        action = self.__get_action_data(fk_acao_id)
        request = UpdateActionRequest.parse_obj(
            json.loads(flask_request.form.get("data"))
        )
        photo_background: Optional[FileStorage] = flask_request.files.get("background")
        photo_banner: Optional[FileStorage] = flask_request.files.get("banner")
        self.__validate_data(request.preenchimento_foto, request.label_foto)

        self.__update_action(request, photo_background, photo_banner, action)
        self.__commit_changes()

        return {"msg": "Ação atualizada com sucesso!"}, 200

    def __get_action_data(self, fk_acao_id: int) -> ActionsLeads:
        action = ActionsLeads.query.filter_by(id=fk_acao_id).first()
        if action is None:
            raise NotFoundError("Ação não encontrada.")

        return action

    def __validate_data(
        self, preenchimento_foto: bool, label_foto: Optional[str]
    ) -> None:
        if preenchimento_foto == True and label_foto is None:
            raise BadRequestError("O preenchimento do campo label foto é obrigatório.")

    def __update_action(
        self,
        request: UpdateActionRequest,
        photo_background: Optional[FileStorage],
        photo_banner: Optional[FileStorage],
        action: ActionsLeads,
    ) -> None:
        action.nome = request.nome
        action.titulo = request.titulo
        action.descricao = request.descricao
        action.status = request.status
        action.preenchimento_foto = request.preenchimento_foto
        action.label_foto = request.label_foto

        if photo_background:
            background_filename = self.__file_service.upload_image(photo_background)
            action.background = background_filename

        if photo_banner:
            banner_filename = self.__file_service.upload_image(photo_banner)
            action.banner = banner_filename

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
