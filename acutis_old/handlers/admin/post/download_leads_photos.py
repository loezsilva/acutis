from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from flask import request as flask_request

from models.foto_leads import FotoLeads
from models.schemas.admin.post.download_leads_photos import DownloadLeadsPhotosRequest
from utils.functions import get_current_time


class DownloadLeadsPhotos:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self):
        request = DownloadLeadsPhotosRequest.parse_obj(flask_request.json)
        self.__register_downloaded_photos(request)
        self.__commit_changes()

        return {"msg": "Fotos de leads baixadas com sucesso!"}, 200

    def __register_downloaded_photos(self, request: DownloadLeadsPhotosRequest) -> None:
        self.__database.session.query(FotoLeads).filter(
            FotoLeads.fk_user_import_id.in_(request.ids_leads)
        ).update(
            {"user_download": current_user["id"], "data_download": get_current_time()},
            synchronize_session=False,
        )

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
