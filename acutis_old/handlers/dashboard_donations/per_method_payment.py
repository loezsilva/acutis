from flask import request
from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal
from typing import List, Dict, Any

from models.campanha import Campanha
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido


class PerMethodPayment:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        self.__http_args = request.args
        self.__data_inicio = self.__http_args.get("data_inicio")
        self.__data_fim = self.__http_args.get("data_fim")

    def execute(self) -> Dict[str, Any]:
        campaigns = self.__get_campaigns()
        payment_methods_data = self.__query_per_methods()

        return {
            "campaigns": campaigns,
            "payment_methods_percentage": payment_methods_data["percentages"],
            "total_donations": payment_methods_data["total_donations"],
            "total_donations_per_method": payment_methods_data["totals"],
        }, 200

    def __get_campaigns(self) -> List[Dict[str, Any]]:
        query = (
            self.__conn.session.query(
                Campanha.titulo.label("campanha_titulo"),
                Campanha.id.label("campanha_id"),
            )
            .join(Pedido, Pedido.fk_campanha_id == Campanha.id)
            .join(ProcessamentoPedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                Campanha.objetivo == "doacao",
                *self.__filter_date(ProcessamentoPedido.data_processamento),
            )
            .distinct(Campanha.id)
        )

        return [
            {"id": campanha.campanha_id, "titulo": campanha.campanha_titulo}
            for campanha in query
        ]

    def __query_per_methods(self) -> Dict[str, Any]:
        subquery_total = (
            self.__conn.session.query(
                self.__conn.func.sum(ProcessamentoPedido.valor).label("total_donations")
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                *self.__filter_date(ProcessamentoPedido.data_processamento),
            )
            .scalar_subquery()
        )

        results = (
            self.__conn.session.query(
                FormaPagamento.descricao.label("forma_pagamento"),
                self.__conn.func.sum(ProcessamentoPedido.valor).label(
                    "total_per_method"
                ),
                (
                    self.__conn.func.sum(ProcessamentoPedido.valor)
                    * 100.0
                    / subquery_total
                ).label("porcentagem"),
            )
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .join(
                FormaPagamento,
                FormaPagamento.id == ProcessamentoPedido.fk_forma_pagamento_id,
            )
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == True,
                ProcessamentoPedido.contabilizar_doacao == True,
                *self.__filter_date(ProcessamentoPedido.data_processamento),
            )
            .group_by(FormaPagamento.descricao)
            .all()
        )

        total_donations = (
            self.__conn.session.query(self.__conn.func.sum(ProcessamentoPedido.valor))
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                ProcessamentoPedido.contabilizar_doacao == 1,
            )
            .scalar()
        )

        expected_methods = ["boleto", "credito", "pix"]
        percentages = {f"{method}_percentage": "0.00" for method in expected_methods}
        totals = {f"total_{method}": "0.00" for method in expected_methods}

        for result in results:
            method_key = result.forma_pagamento.lower().replace(" ", "_")
            percentages[f"{method_key}_percentage"] = self.__format_decimal(
                result.porcentagem
            )
            totals[f"total_{method_key}"] = self.__format_decimal(
                result.total_per_method
            )

        return {
            "percentages": percentages,
            "total_donations": (
                self.__format_decimal(total_donations) if total_donations else "0.00"
            ),
            "totals": totals,
        }

    def __filter_date(self, column):
        from sqlalchemy import and_

        conditions = []
        if self.__data_inicio:
            conditions.append(column >= self.__data_inicio)
        if self.__data_fim:
            conditions.append(column <= self.__data_fim)
        return and_(*conditions) if conditions else [True]

    @staticmethod
    def __format_decimal(value: Decimal) -> str:
        return f"{value:.2f}"
