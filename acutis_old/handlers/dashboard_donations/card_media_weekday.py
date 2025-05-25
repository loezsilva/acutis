from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.campanha import Campanha
from models.pedido import Pedido
from models.perfil import ProfilesEnum
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import calculate_days_interval


class MediaDiariaDonations:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn

    def execute(self) -> dict:

        start_date = (
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
            start_date = start_date.filter(Pedido.anonimo == False)

        start_date = start_date.scalar()

        quantidade_dias = calculate_days_interval(start_date)

        data = self.__querys_values()
        return self.__format_response(data, quantidade_dias)

    def __querys_values(self) -> tuple:
        query = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label(
                    "valor_total"
                ),
                self.__conn.func.count(ProcessamentoPedido.id).label(
                    "quant_pedidos_total"
                ),
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
            query = query.filter(Pedido.anonimo == False)

        query = query.first()

        return query

    def __format_response(
        self, data: tuple, quantidade_de_dias_atual: int
    ) -> tuple:

        valor_total, quant_pedidos_total = data

        media_diaria = valor_total / quantidade_de_dias_atual

        if quant_pedidos_total is not None and quantidade_de_dias_atual > 0:
            media_quantidade_diaria = (
                quant_pedidos_total / quantidade_de_dias_atual
            )
        else:
            media_quantidade_diaria = 0

        return {
            "media_valores_diaria": round(media_diaria, 2),
            "media_quantidade_diaria": int(media_quantidade_diaria),
        }, 200
