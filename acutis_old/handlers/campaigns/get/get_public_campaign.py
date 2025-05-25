from flask_jwt_extended import current_user, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_not_found import NotFoundError
from models.campanha import Campanha
from models.pedido import Pedido
from services.file_service import FileService
from sqlalchemy import and_


class GetPublicCampaign:
    def __init__(self, database: SQLAlchemy, file_service: FileService) -> None:
        self.__database = database
        self.__file_service = file_service

    def execute(self, fk_campanha_id: int):
        campanha = self.__get_public_campaign(fk_campanha_id)
        bloquear_recorrencia_na_campanha = (
            self.__validate_active_recurrence_in_campaign(fk_campanha_id)
        )
        response = self.__prepare_response(campanha, bloquear_recorrencia_na_campanha)
        return response, 200

    def __get_public_campaign(self, fk_campanha_id: int) -> Campanha:
        campanha_query = self.__database.session.query(
            Campanha.titulo,
            Campanha.descricao,
            Campanha.objetivo,
            Campanha.filename,
        ).filter(
            and_(
                Campanha.publica == True,
                Campanha.status == True,
                Campanha.deleted_at.is_(None),
                Campanha.id == fk_campanha_id,
            )
        )

        campanha = campanha_query.first()
        if campanha is None:
            raise NotFoundError("Campanha não encontrada.")

        return campanha

    def __validate_active_recurrence_in_campaign(self, fk_campanha_id: int) -> bool:
        if get_jwt_identity() is not None:
            fk_clifor_id = current_user["fk_clifor_id"]
            doacao_recorrente_na_campanha = Pedido.query.filter(
                Pedido.status_pedido == 1,
                Pedido.recorrencia_ativa == True,
                Pedido.periodicidade == 2,
                Pedido.fk_clifor_id == fk_clifor_id,
                Pedido.fk_campanha_id == fk_campanha_id,
            ).first()
            if doacao_recorrente_na_campanha:
                return True
        return False

    def __get_campaign_image(self, filename: str) -> str:
        url = self.__file_service.get_public_url(filename)
        return url

    def __prepare_response(
        self, campanha: Campanha, bloquear_recorrencia_na_campanha: bool
    ) -> dict:
        response = {
            "titulo": campanha.titulo,
            "descricao": campanha.descricao,
            "objetivo": campanha.objetivo,
            "filename": self.__get_campaign_image(campanha.filename),
            "bloquear_doacao_recorrente": bloquear_recorrencia_na_campanha,
        }
        return response
