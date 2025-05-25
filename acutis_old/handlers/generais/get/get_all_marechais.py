from flask import request
from flask_sqlalchemy import SQLAlchemy
from models.generais import Generais

class ListMarechais:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) :
        marechais = self.__query_marechais()
        return self.__format_response(marechais)

    def __query_marechais(self) -> tuple:
        generais_query: Generais = (
            self.__conn.session.query(Generais.nome, Generais.id)
            .filter(
                Generais.fk_cargo_id ==  1,
                Generais.deleted_at == None,
            )
            .order_by(self.__conn.desc(Generais.created_at))
        )
            
        return generais_query
    
    def __format_response(self, marechais: tuple) -> tuple:
        if marechais is not None:
            res = [
                {
                  "nome": marshal.nome,
                  "id": marshal.id  
                } for marshal in marechais
            ]  
            return res, 200
        
        else:
            return None, 204
