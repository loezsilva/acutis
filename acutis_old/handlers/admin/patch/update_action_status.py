from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.actions_leads import ActionsLeads


class UpdateActionStatus:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database

    def execute(self, fk_acao_id: int):
        action = self.__get_action_data(fk_acao_id)
        self.__update_action_status(action)
        self.__commit_changes()

        return {}, 204

    def __get_action_data(self, fk_acao_id: int) -> ActionsLeads:
        action = ActionsLeads.query.filter_by(id=fk_acao_id).first()
        if action is None:
            raise NotFoundError("Ação não encontrada.")

        return action

    def __update_action_status(self, action: ActionsLeads) -> None:
        action.status = not action.status

    def __commit_changes(self) -> None:
        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
