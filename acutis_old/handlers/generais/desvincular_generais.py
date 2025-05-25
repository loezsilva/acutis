from flask_sqlalchemy import SQLAlchemy
from exceptions import errors_handler
from models.generais import Generais


class DesvincularGenerais:
    def __init__(self, fk_marechal_id: int, db: SQLAlchemy):
        self.__fk_marechal_id = fk_marechal_id
        self.__db = db

    def execute(self):
        try:
            Generais.query.filter(Generais.fk_usuario_superior_id == self.__fk_marechal_id).update(
                {Generais.fk_usuario_superior_id: None}, synchronize_session=False
            )
            
            self.__db.session.commit()
            
        except Exception as e:
            self.__db.session.rollback()   
            return errors_handler(e)   