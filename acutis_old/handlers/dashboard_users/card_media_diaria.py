from datetime import datetime
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from models.usuario import Usuario
import logging

from utils.functions import calculate_days_interval, get_current_time

class MediaCadastrosDiarios:
    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        self.__hoje = get_current_time()

    def execute(self) -> tuple:
        media_diaria, cadastros_hoje = self.__calcular_media_cadastros()
        return self.__format_response(cadastros_hoje, media_diaria)

    def __calcular_media_cadastros(self) -> tuple:
        start_date = (
            self.__conn.session.query(self.__conn.func.min(Usuario.data_criacao))
            .filter(
                Usuario.deleted_at == None,
            )
            .scalar()
        )
         
        dias = calculate_days_interval(start_date)
        
        total_cadastros_ano = self.__get_total_cadastros()
        cadastros_dia_atual = self.__get_cadastros_dia_atual()
        media_diaria = total_cadastros_ano / dias  

        return int(media_diaria), cadastros_dia_atual

    def __get_total_cadastros(self) -> int:
        return (
            self.__conn.session.query(self.__conn.func.count(Usuario.id).label("total"))
            .filter(
                Usuario.deleted_at == None,
            )
            .first()[0]
        )

    def __get_cadastros_dia_atual(self) -> int: 
        return (
            self.__conn.session.query(Usuario)
            .filter(
                self.__conn.func.year(Usuario.data_criacao) == self.__hoje.year,
                self.__conn.func.month(Usuario.data_criacao) == self.__hoje.month,
                self.__conn.func.day(Usuario.data_criacao) == self.__hoje.day,
                Usuario.deleted_at == None,
            )
            .count()
        )

    def __format_response(self, quantidade: int, media: str) -> tuple:
        return {
            "cadastros_hoje": quantidade,
            "media_diaria": media,
        }, 200
