from datetime import datetime, time
import logging
from typing import Dict

from flask import request as FlaskRequest

from models.view_avulsas import ViewAvulsas
from models.view_recorrentes import ViewRecorrentes
from builder import db


class UpdateLive:
    def __init__(self) -> None:
        pass

    def execute(self, request: FlaskRequest, programacao_id: int):  # type: ignore
        try:
            PROGRAMACAO_MAP = {
                "avulsa": self.__update_single_live,
                "periodica": self.__update_periodic_live,
            }
            body: Dict = request.json
            tipo: str = (body["tipo_programacao"]).lower()

            if tipo not in ["avulsa", "periodica"]:
                return {
                    "error": "O tipo de programação informada é inválida."
                }, 400

            update_live = PROGRAMACAO_MAP[tipo]

            return update_live(body, programacao_id)
        except KeyError as err:
            return {"error": f"O campo {err} é obrigatório."}, 400

        except Exception as err:
            db.session.rollback()
            logging.error(f"{str(type(err))} - {str(err)}")
            return {
                "error": "Ocorreu um erro ao atualizar a programação da live."
            }, 500

    def __update_single_live(self, body: Dict, programacao_id: int):
        live_avulsa = db.session.get(ViewAvulsas, programacao_id)
        if not live_avulsa:
            return {"error": "Programação da live não encontrada."}, 404

        data_hora_inicio: datetime = body["data_hora_inicio"]

        live_avulsa.data_hora_inicio = data_hora_inicio

        db.session.commit()

        return {"msg": "Programação da live atualizada com sucesso."}, 200

    def __update_periodic_live(self, body: Dict, programacao_id: int):
        DIAS_DA_SEMANA = [
            "domingo",
            "segunda-feira",
            "terca-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sabado",
        ]

        live_periodica = db.session.get(ViewRecorrentes, programacao_id)
        if not live_periodica:
            return {"error": "Programação da live não encontrada."}, 404

        data_hora_inicio: time = body["data_hora_inicio"]
        dia_semana: str = (body["dia_semana"]).lower()

        if dia_semana not in DIAS_DA_SEMANA:
            return {"error": "O dia da semana está inválido."}, 400

        live_periodica.data_hora_inicio = data_hora_inicio
        live_periodica.dia_semana = dia_semana

        db.session.commit()

        return {"msg": "Programação da live atualizada com sucesso."}, 200
