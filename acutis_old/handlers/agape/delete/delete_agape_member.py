from http import HTTPStatus
from flask_sqlalchemy import SQLAlchemy
from models.agape.membro_agape import MembroAgape


class DeleteAgapeMember:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_membro_agape_id: int):
        self.__delete_member(fk_membro_agape_id)
        return {}, HTTPStatus.NO_CONTENT

    def __delete_member(self, fk_membro_agape_id: int):
        self.__database.session.query(MembroAgape).filter(
            MembroAgape.id == fk_membro_agape_id
        ).delete(synchronize_session=False)
        self.__database.session.commit()
