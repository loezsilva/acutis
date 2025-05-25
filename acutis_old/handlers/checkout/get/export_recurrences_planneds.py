from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, Date
from utils.export_excel import export_excel
from utils.functions import get_current_time, last_day_of_month
from models import Campanha, Clifor, FormaPagamento, ProcessamentoPedido, Pedido


class ExportRecurrencesPlanned:

    def __init__(self, conn: SQLAlchemy):
        self.__conn = conn
        self.__current_date = get_current_time()
        self.__http_request = request.args

        self.__filter_nome = self.__http_request.get("nome")
        self.__data_inicio = self.__http_request.get("data_inicio")
        self.__data_fim = self.__http_request.get("data_fim")
        self.__filter_metodo = self.__http_request.get("forma_pagamento")
        self.__filter_campanha = self.__http_request.get("campanha_id")

    def execute(self):
        data = self.__query_donations_previstas()
        return self.__format_response(data)

    def __query_donations_previstas(self):

        ultimo_dia_mes_atual = last_day_of_month(
            self.__current_date.year, self.__current_date.month
        )

        all_donations_actual_month = (
            self.__conn.session.query(ProcessamentoPedido.fk_pedido_id)
            .filter(
                self.__conn.extract("month", ProcessamentoPedido.data_processamento)
                == self.__current_date.month,
                self.__conn.extract("year", ProcessamentoPedido.data_processamento)
                == self.__current_date.year,
                ProcessamentoPedido.status_processamento == 1,
            )
            .subquery()
        )

        data_pedido_modificado = cast(
            self.__conn.func.concat(
                self.__current_date.year,
                "-",
                self.__conn.func.right(
                    self.__conn.func.concat(
                        "0", cast(self.__current_date.month, self.__conn.String)
                    ),
                    2,
                ),
                "-",
                self.__conn.func.right(
                    self.__conn.func.concat(
                        "0",
                        cast(
                            self.__conn.case(
                                (
                                    self.__conn.func.day(Pedido.data_pedido)
                                    > ultimo_dia_mes_atual,
                                    ultimo_dia_mes_atual,
                                ),
                                else_=self.__conn.func.day(Pedido.data_pedido),
                            ),
                            self.__conn.String,
                        ),
                    ),
                    2,
                ),
            ),
            Date,
        )

        query_previstas = (
            self.__conn.session.query(
                Pedido.id.label("pedido_id"),
                Clifor.id.label("clifor_id"),
                Clifor.nome,
                Clifor.cpf_cnpj,
                Pedido.data_pedido,
                Pedido.valor_total_pedido,
                data_pedido_modificado.label("data_pedido_modificado"),
                Campanha.titulo.label("nome_campanha"),
                Campanha.descricao,
                FormaPagamento.descricao.label("metodo_pagamento"),
            )
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(FormaPagamento, FormaPagamento.id == Pedido.fk_forma_pagamento_id)
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .filter(
                (
                    (FormaPagamento.id == self.__filter_metodo)
                    if self.__filter_metodo
                    else True
                ),
                (
                    (Campanha.id == self.__filter_campanha)
                    if self.__filter_campanha
                    else True
                ),
                (
                    (Clifor.nome.ilike(f"%{self.__filter_nome}%"))
                    if self.__filter_nome
                    else True
                ),
                (
                    (data_pedido_modificado >= self.__data_inicio)
                    if self.__data_inicio
                    else True
                ),
                (
                    (data_pedido_modificado <= self.__data_fim)
                    if self.__data_fim
                    else True
                ),
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == 1,
                self.__conn.func.day(Pedido.data_pedido)
                >= self.__conn.func.day(self.__conn.func.now()),
                Pedido.id.notin_(all_donations_actual_month),
            )
            .order_by(
                self.__conn.func.concat(
                    self.__conn.func.right(
                        self.__conn.func.concat(
                            "0",
                            self.__conn.cast(
                                self.__conn.func.day(Pedido.data_pedido),
                                self.__conn.String,
                            ),
                        ),
                        2,
                    ),
                    "/",
                    self.__conn.func.right(
                        self.__conn.func.concat(
                            "0",
                            self.__conn.cast(
                                self.__current_date.month, self.__conn.String
                            ),
                        ),
                        2,
                    ),
                    "/",
                    self.__current_date.year,
                ).asc()
            )
        )

        return query_previstas.all()

    def __format_response(self, data: tuple) -> tuple:
        list_donations_recurrence_previstas = [
            {
                "Pedido_id": donation.pedido_id,
                "Clifor_id": donation.clifor_id,
                "Nome": donation.nome,
                "CPF/CNPJ": donation.cpf_cnpj,
                "Data": donation.data_pedido_modificado.strftime("%d-%m-%Y"),
                "Valor": round(donation.valor_total_pedido, 2),
                "Metodo_pagamento": donation.metodo_pagamento,
                "Campanha": donation.nome_campanha,
            }
            for donation in data
        ]

        return export_excel(
            list_donations_recurrence_previstas, "doacoes-recorrentes-previstas"
        )
