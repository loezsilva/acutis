from flask import request
from sqlalchemy import between, func
from models.usuario import Usuario
from utils.functions import get_current_time, last_day_of_month
from builder import db
from models import (
    Pedido,
    Clifor,
    Campanha,
    ProcessamentoPedido,
    FormaPagamento,
)


class ListingRecurrenceNotPaid:
    def __init__(self) -> None:
        self.__current_date = get_current_time()
        self.__http_request = request.args

        self.__page = self.__http_request.get("page", 1, type=int)
        self.__per_page = self.__http_request.get("per_page", 10, type=int)

        self.__filter_nome = self.__http_request.get("nome")
        self.__data_inicio = self.__http_request.get("data_inicio")
        self.__data_fim = self.__http_request.get("data_fim")
        self.__filter_metodo = self.__http_request.get("forma_pagamento")
        self.__filter_campanha = self.__http_request.get("filter_campanha")

    def execute(self):
        orders, total_sum, quantidade = self.__query()
        return self.__format_response(orders, total_sum, quantidade)

    def __query(self):
        
        ultimo_dia_mes_atual = last_day_of_month(
            get_current_time().year, get_current_time().month
        )
        
        processed_orders_subquery = (
            db.session.query(ProcessamentoPedido.fk_pedido_id)
            .join(Pedido, ProcessamentoPedido.fk_pedido_id == Pedido.id)
            .filter(
                db.func.month(ProcessamentoPedido.data_processamento)
                == self.__current_date.month,
                db.func.year(ProcessamentoPedido.data_processamento)
                == self.__current_date.year,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
            )
            .subquery()
        )

        subquery_max_processamento = (
            db.session.query(
                ProcessamentoPedido.fk_pedido_id,
                db.func.max(ProcessamentoPedido.id).label(
                    "max_processamento_id"
                ),
            )
            .group_by(ProcessamentoPedido.fk_pedido_id)
            .subquery()
        )
        
        data_pedido_ajusted = ( db.func.concat(
                    self.__current_date.year,
                    "-",
                    db.func.right(
                        db.func.concat("0", db.cast(self.__current_date.month, db.String)),
                        2,
                    ),
                    "-",
                    db.func.right(
                        db.func.concat(
                            "0",
                            db.cast(
                                db.case(
                                    (
                                        db.func.day(Pedido.data_pedido) > ultimo_dia_mes_atual,
                                        ultimo_dia_mes_atual,
                                    ),
                                    else_=db.func.day(Pedido.data_pedido),
                                ),
                                db.String,
                            ),
                        ),
                        2,
                    ),
                )
        ).label("data_pedido_ajusted")

        orders = (
            db.session.query(
                Pedido.id.label("pedido_id"),
                Clifor.id.label("clifor_id"),
                Clifor.nome,
                Clifor.cpf_cnpj,
                func.format(Pedido.data_pedido, "dd/MM/yyyy HH:mm:ss").label(
                    "data_pedido"
                ),
                Pedido.valor_total_pedido,
                data_pedido_ajusted,
                Campanha.titulo.label("nome_campanha"),
                Campanha.descricao,
                FormaPagamento.descricao.label("metodo_pagamento"),
                ProcessamentoPedido.id.label("fk_processamento_pedido_id"),
                func.format(
                    ProcessamentoPedido.data_lembrete_doacao,
                    "dd/MM/yyyy HH:mm:ss",
                ).label("data_lembrete_doacao"),
                Usuario.nome.label("lembrete_enviado_por"),
            )
            .join(
                subquery_max_processamento,
                Pedido.id == subquery_max_processamento.c.fk_pedido_id,
            )
            .join(
                ProcessamentoPedido,
                ProcessamentoPedido.id
                == subquery_max_processamento.c.max_processamento_id,
            )
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(
                FormaPagamento,
                FormaPagamento.id == Pedido.fk_forma_pagamento_id,
            )
            .join(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .outerjoin(
                Usuario, Usuario.id == ProcessamentoPedido.lembrete_enviado_por
            )
            .filter(
                (
                    db.func.cast(data_pedido_ajusted, db.Date).between(
                        db.func.cast(self.__data_inicio, db.Date),
                        db.func.cast(self.__data_fim, db.Date)
                    ) if self.__data_inicio and self.__data_fim
                    else True
                ),
                Pedido.contabilizar_doacao == 1,
                Pedido.periodicidade == 2,
                Pedido.recorrencia_ativa == 1,
                db.func.day(Pedido.data_pedido)
                < db.func.day(self.__current_date),
                Pedido.id.notin_(processed_orders_subquery),
                (
                    Clifor.nome.ilike(f"%{self.__filter_nome}%")
                    if self.__filter_nome
                    else True
                ),
                (
                    Campanha.id == self.__filter_campanha
                    if self.__filter_campanha
                    else True
                ),
                (
                    FormaPagamento.id == self.__filter_metodo
                    if self.__filter_metodo
                    else True
                ),
            )
            .order_by(db.desc(data_pedido_ajusted))
        )

        result = (
            db.session.query(
                db.func.coalesce(
                    db.func.sum(Pedido.valor_total_pedido), 0
                ).label("total_sum"),
                db.func.count(Pedido.id).label("total_count"),
            )
            .filter(orders.whereclause)
            .first()
        )

        total_sum = result.total_sum if result else 0
        quant_pedido = result.total_count if result else 0

        paginate = orders.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )

        return paginate, total_sum, quant_pedido

    def __format_response(self, orders, total_sum, quantidade):
        list_orders = [
            {
                "pedido_id": donation.pedido_id,
                "clifor_id": donation.clifor_id,
                "nome": donation.nome,
                "cpf_cnpj": donation.cpf_cnpj,
                "data_prevista": donation.data_pedido_ajusted,
                "valor": str(round(donation.valor_total_pedido, 2)),
                "metodo_pagamento": donation.metodo_pagamento,
                "campanha": donation.nome_campanha or "",
                "descricao_campanha": donation.descricao or "",
                "pedido_criado_em": donation.data_pedido,
                "processamento_pedido": donation.fk_processamento_pedido_id,
                "data_lembrete_doacao": donation.data_lembrete_doacao,
                "lembrete_enviado_por": donation.lembrete_enviado_por,
            }
            for donation in orders.items
        ]

        pagination = {
            "total_pages": orders.pages,
            "current_page": self.__page,
            "per_page": self.__per_page,
            "total_items": orders.total,
        }

        info_card = {
            "valor_total": str(round(total_sum, 2)),
            "total_items": quantidade,
        }

        response = {
            "lista": list_orders,
            "pagination": pagination,
            "info_card": info_card,
        }

        return response, 200
