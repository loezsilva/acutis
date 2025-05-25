from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

from models.campanha import Campanha
from models.pedido import Pedido
from models.perfil import ProfilesEnum
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time


class MediaMensalDonations:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn

    def execute(self) -> dict:
        data = self.__querys_values()
        return self.__format_response(data)

    def __querys_values(self) -> list:
        query_mensal = (
            self.__conn.session.query(
                self.__conn.func.count(ProcessamentoPedido.id).label(
                    "quant_mensal"
                ),
                self.__conn.func.month(
                    ProcessamentoPedido.data_processamento
                ).label("mes"),
                self.__conn.func.sum(ProcessamentoPedido.valor).label(
                    "valor_mensal"
                ),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.or_(
                    Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)
                ),
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
            )
            .group_by(
                self.__conn.func.month(ProcessamentoPedido.data_processamento)
            )
            .order_by(
                self.__conn.func.month(ProcessamentoPedido.data_processamento)
            )
        )

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            query_mensal = query_mensal.filter(Pedido.anonimo == False)

        return query_mensal.all()

    def __format_response(self, resultados: list) -> dict:
        if not resultados:
            return {"media_valor_mensal": 0, "media_quant_mensal": 0}

        soma_total_valor = sum(
            resultado.valor_mensal for resultado in resultados
        )
        soma_total_quant = sum(
            resultado.quant_mensal for resultado in resultados
        )

        quantidade_meses = len(resultados)

        media_valor_mensal = (
            soma_total_valor / quantidade_meses if quantidade_meses > 0 else 0
        )
        media_quant_mensal = (
            soma_total_quant / quantidade_meses if quantidade_meses > 0 else 0
        )

        return {
            "media_valor_mensal": round(media_valor_mensal, 2),
            "media_quant_mensal": int(media_quant_mensal),
        }
