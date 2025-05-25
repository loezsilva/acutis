from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from models.campanha import Campanha
from models.pedido import Pedido
from models.perfil import ProfilesEnum
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import calculate_days_interval, get_current_time


class TotalDonationsActualDay:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn

    def execute(self) -> dict:
        data = self.__querys_values()
        return self.__format_response(data)

    def __querys_values(self) -> tuple:

        start_date_query = (
            self.__conn.session.query(
                self.__conn.func.min(ProcessamentoPedido.data_processamento)
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
            )
        )

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            start_date_query = start_date_query.filter(Pedido.anonimo == False)

        start_date = start_date_query.scalar()

        quantidade_dias = calculate_days_interval(start_date)

        query_total = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label(
                    "valor_total"
                )
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.or_(
                    Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)
                ),
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
            )
        )

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            query_total = query_total.filter(Pedido.anonimo == False)

        query_total = query_total.first()

        media_diaria = (
            query_total[0] / quantidade_dias if quantidade_dias > 0 else 0
        )

        query_dia_atual = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label(
                    "valor_total"
                ),
                self.__conn.func.count(ProcessamentoPedido.id).label(
                    "quant_pedidos"
                ),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
                Pedido.contabilizar_doacao == 1,
                self.__conn.cast(
                    ProcessamentoPedido.data_processamento, self.__conn.Date
                )
                == self.__conn.cast(get_current_time(), self.__conn.Date),
                self.__conn.or_(
                    Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)
                ),
            )
        )

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            query_dia_atual = query_dia_atual.filter(Pedido.anonimo == False)

        valor_total, quant_pedidos = query_dia_atual.first()

        return media_diaria, valor_total, quant_pedidos

    def __format_response(self, data: tuple) -> tuple:
        media_diaria, valor_total, quant_pedidos = data

        valor_total = valor_total or 0
        quant_pedidos = quant_pedidos or 0
        media_diaria = media_diaria or 0

        if media_diaria > 0 and valor_total:
            porcentagem_dia = ((valor_total * 100) / media_diaria) - 100
        else:
            porcentagem_dia = 0

        response = {
            "valor_total": round(valor_total, 2),
            "quant_pedidos": quant_pedidos,
            "porcentagem_dia": round(porcentagem_dia, 2),
            "media_diaria": round(media_diaria, 2),
        }

        return response, 200
