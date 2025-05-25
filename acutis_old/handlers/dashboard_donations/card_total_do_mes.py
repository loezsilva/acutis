from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy
from models.campanha import Campanha
from models.pedido import Pedido
from models.perfil import ProfilesEnum
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time
from utils.functions import calculate_months_interval


class TotalDonationsActualMonth:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn

    def execute(self) -> dict:
        data = self.__querys_values()
        return self.__format_response(data)

    def __querys_values(self) -> tuple:

        end_date = get_current_time()

        date_first_donation = (
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
            date_first_donation = date_first_donation.filter(
                Pedido.anonimo == False
            )

        date_first_donation = date_first_donation.scalar()

        query_valor_total = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor)
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .filter(
                ProcessamentoPedido.data_processamento.between(
                    date_first_donation, end_date
                ),
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
            )
        )

        query_mes_atual = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label(
                    "valor_total_mes"
                ),
                self.__conn.func.count(ProcessamentoPedido.id).label(
                    "quant_pedidos_mes"
                ),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .outerjoin(Campanha, Pedido.fk_campanha_id == Campanha.id)
            .filter(
                self.__conn.func.year(ProcessamentoPedido.data_processamento)
                == get_current_time().year,
                self.__conn.func.month(ProcessamentoPedido.data_processamento)
                == get_current_time().month,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
                self.__conn.extract(
                    "year", ProcessamentoPedido.data_processamento
                )
                == get_current_time().year,
                self.__conn.or_(
                    Campanha.contabilizar_doacoes == 1, Campanha.id.is_(None)
                ),
            )
        )

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            query_valor_total = query_valor_total.filter(
                Pedido.anonimo == False
            )
            query_mes_atual = query_mes_atual.filter(Pedido.anonimo == False)

        query_valor_total = query_valor_total.scalar()
        query_mes_atual = query_mes_atual.one_or_none()

        return (query_mes_atual, query_valor_total, date_first_donation)

    def __format_response(self, query: tuple) -> tuple:

        query_mes, query_total, date_first_donation = query

        valor_total_mes = query_mes.valor_total_mes if query_mes else 0
        quant_pedidos_mes = query_mes.quant_pedidos_mes if query_mes else 0

        meses_ate_agora = calculate_months_interval(date_first_donation)

        media_mensal = (
            query_total / meses_ate_agora if meses_ate_agora > 0 else 0
        )
        if media_mensal > 0:
            porcentagem_valor_mes = (
                (valor_total_mes * 100) / media_mensal
            ) - 100
        else:
            porcentagem_valor_mes = 0

        return {
            "valor_total_mes": (
                round(valor_total_mes, 2) if valor_total_mes else 0.0
            ),
            "quant_pedidos_mes": quant_pedidos_mes,
            "media_mensal": round(media_mensal, 2) if media_mensal else 0.0,
            "porcentagem_valor_mes": (
                round(porcentagem_valor_mes, 2)
                if porcentagem_valor_mes
                else 0.0
            ),
        }, 200
