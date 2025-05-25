from flask_sqlalchemy import SQLAlchemy
from python_http_client import NotFoundError
from exceptions.errors_handler import errors_handler
from handlers.generais.desvincular_generais import DesvincularGenerais
from models.generais import Generais

class DeleteGeneral:
    def __init__(self, general_id: int, db: SQLAlchemy):
        self.__general_id = general_id
        self.__db = db
    
    def execute(self) -> tuple:
        general = self.__get_general()
        self.__delete(general)
        return self.__format_response()
    
    def __get_general(self):
        general: Generais = Generais.query.get(self.__general_id)
        
        if general is None:
            raise NotFoundError("General não encontrado")
        
        return general

    def __delete(self, general: Generais):
        try:
            if general.fk_cargo_id == 1:
                desvincular_generais = DesvincularGenerais(general.id, self.__db)
                desvincular_generais.execute()
            general.soft_delete()
        except Exception as e:
            self.__db.session.rollback()
            return errors_handler(e)
        
    def __format_response(self) -> tuple:
        return {"msg": "General deletado com sucesso."}, 200