from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from models.endereco import Endereco
from models.clifor import Clifor

class UsersByState:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        try:
            users_by_state = self.__get_users_by_state()
            response = self.__format_response(users_by_state)
            return response
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def __get_users_by_state(self) -> list:
        return (
            self.__conn.session.query(
                Endereco.estado,
                self.__conn.func.count(Usuario.id)
            )
            .join(Clifor, Clifor.id == Endereco.fk_clifor_id)
            .join(Usuario, Usuario.id == Clifor.fk_usuario_id)
            .filter(Endereco.estado != None, Usuario.deleted_at == None)
            .group_by(Endereco.estado)
            .all()
        )

    def __format_response(self, users_by_state: list) -> tuple:
        users_by_state_dict = {state: count for state, count in users_by_state}

        return jsonify({"users_by_state": users_by_state_dict}), 200
