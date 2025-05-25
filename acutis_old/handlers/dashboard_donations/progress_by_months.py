from flask import request
from flask_sqlalchemy import SQLAlchemy

from models.processamento_pedido import ProcessamentoPedido
from models.pedido import Pedido

class ProgressByMonths:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__http_args = request.args
        self.__conn = conn
        
        self.__campanha_id = self.__http_args.get("fk_campanha_id")
        self.__forma_pagamento = self.__http_args.get("forma_pagamento")

    def execute(self) -> tuple:
        data = self.__query_amounts_values()
        return self.__format_response(data)

    def __query_amounts_values(self) -> tuple:
        monthly_totals = (
            self.__conn.session.query(
                self.__conn.func.concat(
                    self.__conn.func.year(ProcessamentoPedido.data_processamento),
                    '-',
                    self.__conn.func.right(
                        '0' + self.__conn.func.cast(
                            self.__conn.func.month(ProcessamentoPedido.data_processamento), 
                            self.__conn.String
                        ), 
                        2
                    ) 
                ).label('ano_mes'),
                self.__conn.func.sum(ProcessamentoPedido.valor).label('total_doacoes')
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .filter(
                Pedido.fk_campanha_id == self.__campanha_id if self.__campanha_id else True,
                Pedido.fk_forma_pagamento_id == self.__forma_pagamento if self.__forma_pagamento else True,
                self.__conn.func.year(ProcessamentoPedido.data_processamento) == 
                self.__conn.func.year(self.__conn.func.current_date()),
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.contabilizar_doacao == 1
            )
            .group_by(
                self.__conn.func.year(ProcessamentoPedido.data_processamento),
                self.__conn.func.month(ProcessamentoPedido.data_processamento)
            )
            .subquery()
        )

        donation_growth = (
            self.__conn.session.query(
                monthly_totals.c.ano_mes,
                monthly_totals.c.total_doacoes,
                self.__conn.func.coalesce(
                    (
                        monthly_totals.c.total_doacoes - 
                        self.__conn.func.lag(monthly_totals.c.total_doacoes).over(order_by=monthly_totals.c.ano_mes)
                    ) / 
                    self.__conn.func.lag(monthly_totals.c.total_doacoes).over(order_by=monthly_totals.c.ano_mes) * 100,
                    0
                ).label('percentual')
            )
            .order_by(monthly_totals.c.ano_mes)
        )

        return donation_growth

    def __format_response(self, data: tuple) -> tuple:
        res = [
            {
              "ano_mes": item.ano_mes,
              "total_doacoes": str(round(item.total_doacoes, 2)),
              "porcentage": str(round(item.percentual, 2))
            } for item in data
        ]
        
        return res, 200
            