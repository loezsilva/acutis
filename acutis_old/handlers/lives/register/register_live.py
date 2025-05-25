from datetime import datetime, time
import logging
from typing import Dict, List
from flask import request as FlaskRequest

from models.view_avulsas import ViewAvulsas
from builder import db
from models.view_recorrentes import ViewRecorrentes


class RegisterLive:
    def __init__(self) -> None:
        pass

    def execute(self, request: FlaskRequest):  # type: ignore
        try:
            body = request.json

            tipo = (body["tipo"].strip()).lower()

            match tipo:
                case "avulsa":
                    return self.__register_single_lives(body)
                case "periodica":
                    return self.__register_periodic_lives(body)
                case _:
                    return {"error": "Tipo de programação inválida."}, 400
        except KeyError as err:
            return {"error": f"O campo {err} é obrigatório."}, 400

        except Exception as err:
            db.session.rollback()
            logging.error(f"{str(type(err))} - {str(err)}")
            return {"error": "Ocorreu um erro ao cadastrar as lives."}, 500

    def __register_single_lives(self, body: Dict):
        data_hora_inicio: datetime = body["data_hora_inicio"]
        canais_ids: List[int] = body["canais_ids"]

        lives = [
            {"data_hora_inicio": data_hora_inicio, "fk_view_live_id": canal_id}
            for canal_id in canais_ids
        ]

        db_lives_avulsas = [ViewAvulsas(**live) for live in lives]
        db.session.add_all(db_lives_avulsas)

        db.session.commit()

        return {"msg": "Lives cadastradas com sucesso."}, 201

    def __register_periodic_lives(self, body: Dict):
        canais_ids: List[int] = body["canais_ids"]
        programacoes: List[Dict] = body["programacoes"]

        for programacao in programacoes:
            dia_semana: str = programacao["dia_semana"]
            data_hora_inicio: str | time = programacao["data_hora_inicio"]

            lives_periodicas = [
                {
                    "dia_semana": dia_semana,
                    "data_hora_inicio": data_hora_inicio,
                    "fk_view_live_id": canal_id,
                }
                for canal_id in canais_ids
            ]

            db_lives_periodicas = [
                ViewRecorrentes(**live_periodica)
                for live_periodica in lives_periodicas
            ]
            db.session.add_all(db_lives_periodicas)

        db.session.commit()

        return {"msg": "Lives cadastradas com sucesso."}, 201
