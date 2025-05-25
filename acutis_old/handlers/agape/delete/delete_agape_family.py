from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from exceptions.error_types.http_not_found import NotFoundError
from models.agape.familia_agape import FamiliaAgape
from models.agape.membro_agape import MembroAgape
from utils.functions import get_current_time


class DeleteAgapeFamily:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_familia_agape_id: int):
        try:
            familia = self.__get_agape_family_data(fk_familia_agape_id)
            self.__delete_family_and_members(familia)
        except Exception as exception:
            self.__database.session.rollback()
            raise exception

        return {}, HTTPStatus.NO_CONTENT

    def __get_agape_family_data(self, fk_familia_agape_id: int):
        familia: FamiliaAgape = self.__database.session.get(
            FamiliaAgape, fk_familia_agape_id
        )
        if familia is None or familia.deleted_at is not None:
            raise NotFoundError("Família não encontrada.")
        return familia

    def __delete_family_and_members(self, familia: FamiliaAgape):
        self.__database.session.query(MembroAgape).filter(
            MembroAgape.fk_familia_agape_id == familia.id
        ).delete(synchronize_session=False)

        familia.deleted_at = get_current_time()
        familia.status = False
        self.__database.session.commit()
