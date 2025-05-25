from datetime import datetime
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import case
from models.campanha import Campanha
from models.clifor import Clifor
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time, last_day_of_month


class DonationsPlanned:
    def __init__(self, conn: SQLAlchemy) -> None:
        self.__conn = conn
        self.__http_request = request.args
        self.__current_date = get_current_time()

        self.__filter_nome = self.__http_request.get("nome")
        self.__data_inicio = self.__http_request.get("data_inicio")
        self.__data_fim = self.__http_request.get("data_fim")
        self.__filter_metodo = self.__http_request.get("forma_pagamento")
        self.__filter_campanha = self.__http_request.get("campanha_id")

        self.__page = self.__http_request.get("page", 1, type=int)
        self.__per_page = self.__http_request.get("per_page", 10, type=int)

    def execute(self):
        donations_made_ids = self.__get_donations_made()
        donations = self.__query_donations_planned(donations_made_ids)
        response = self.__format_response(donations)
        return response

    def __get_donations_made(self):
        donations_made = (
            self.__conn.session.query(ProcessamentoPedido.fk_pedido_id)
            .filter(
                self.__conn.extract("month", ProcessamentoPedido.data_processamento)
                == self.__current_date.month,
                self.__conn.extract("year", ProcessamentoPedido.data_processamento)
                == self.__current_date.year,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
            )
            .subquery()
        )

        return donations_made

    def __query_donations_planned(self, donations_mades_ids):
        ultimo_dia_mes_atual = last_day_of_month(
            self.__current_date.year, self.__current_date.month
        )

        data_pedido_modificado = self.__conn.func.concat(
            self.__current_date.year,
            "-",
            self.__conn.func.right(
                self.__conn.func.concat(
                    "0",
                    self.__conn.cast(self.__current_date.month, self.__conn.String),
                ),
                2,
            ),
            "-",
            self.__conn.func.right(
                self.__conn.func.concat(
                    "0",
                    self.__conn.cast(
                        case(
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
        )

        query = (
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
            .join(
                FormaPagamento,
                FormaPagamento.id == Pedido.fk_forma_pagamento_id,
            )
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .filter(
                (
                    FormaPagamento.id == self.__filter_metodo
                    if self.__filter_metodo
                    else True
                ),
                (
                    Campanha.id == self.__filter_campanha
                    if self.__filter_campanha
                    else True
                ),
                (
                    Clifor.nome.ilike(f"%{self.__filter_nome}%")
                    if self.__filter_nome
                    else True
                ),
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == 1,
                self.__conn.func.day(Pedido.data_pedido)
                >= self.__conn.func.day(self.__conn.func.now()),
                Pedido.id.notin_(donations_mades_ids),
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

        if self.__data_inicio:
            query = query.filter(data_pedido_modificado >= self.__data_inicio)

        if self.__data_fim:
            query = query.filter(data_pedido_modificado <= self.__data_fim)

        res = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )

        return res

    def __format_response(self, data: tuple) -> tuple:

        res = [
            {
                "pedido_id": donation.pedido_id,
                "clifor_id": donation.clifor_id,
                "nome": donation.nome,
                "data_donation": datetime.strptime(
                    donation.data_pedido_modificado, "%Y-%m-%d"
                ).strftime("%d/%m/%Y"),
                "valor": str(round(donation.valor_total_pedido, 2)),
                "metodo_pagamento": donation.metodo_pagamento,
                "campanha": donation.nome_campanha,
            }
            for donation in data
        ]

        paginate = {
            "current_page": self.__page,
            "per_page": self.__per_page,
            "total_items": data.total,
            "pages": data.pages,
        }

        response = {"lista": res, "pagination": paginate}

        return response, 200
