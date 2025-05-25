from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
from utils.functions import get_current_time
from utils.functions import get_current_time
import pytz

class CadastrosMediaMensal:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn

    def execute(self) -> tuple:
        cadastros_mes, media_mensal = self.__calcular_media_mensal()

        response = {
            "cadastros_mes": cadastros_mes,
            "media_mensal": media_mensal,
        }
        return jsonify(response), 200

    def __calcular_media_mensal(self) -> tuple:

        cadastros_mes = self.__get_cadastros_mes()
        total_cadastros, meses_ate_hoje = self.__get_total_cadastros()
        media_mensal = total_cadastros / meses_ate_hoje if meses_ate_hoje > 0 else 0

        return cadastros_mes, int(media_mensal)

    def __get_cadastros_mes(self) -> int:
        hoje = get_current_time()
        return (
            self.__conn.session.query(
                self.__conn.func.count(Usuario.id)
            )
            .filter(
                Usuario.deleted_at == None,
                self.__conn.func.month(Usuario.data_criacao) == self.__conn.func.month(hoje),
                self.__conn.func.year(Usuario.data_criacao) == self.__conn.func.year(hoje),
            ).first()[0]
        )

    def __get_total_cadastros(self) -> tuple:
        """Consulta o número total de cadastros no ano"""
        total_cadastros, primeira_data_criacao = (
            self.__conn.session.query(
                self.__conn.func.count(Usuario.id).label("total_cadastros"),
                self.__conn.func.min(Usuario.data_criacao).label("primeira_data_criacao")
            )
            .filter(
                Usuario.deleted_at == None
            )
            .first()   
        )

        return (
            total_cadastros,
            (
                get_current_time() - pytz.UTC.localize(primeira_data_criacao)
            ).days // 30,
        )
        
        
