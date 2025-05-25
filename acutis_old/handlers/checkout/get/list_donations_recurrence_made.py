from builder import db
from models import (
    Clifor,
    Campanha,
    Pedido,
    FormaPagamento,
    ProcessamentoPedido,
)
from utils.functions import get_current_time
from flask import request
import logging


class RecurrenceDonationsMade:
    def __init__(self) -> None:
        self.__data = request.args

        self.__page = self.__data.get("page", 1, type=int)
        self.__per_page = self.__data.get("per_page", 10, type=int)

    def execute(self):
        try:
            return self.__get_donations_recurrence_made()
        except Exception as err:
            logging.error(
                f"ERROR -> LISTA RECORRENTES EFETUADAS - {type(err)} - {err}"
            )
            return {
                "error": "Não foi possivel listar doações recorrentes do mês"
            }, 500

    def __query_total_and_quant_recurrence(self):
        query_quant = (
            db.session.query(
                db.func.count(ProcessamentoPedido.id).label("quant"),
                db.func.sum(ProcessamentoPedido.valor).label("valor_total"),
            )
            .join(Pedido, Pedido.id == ProcessamentoPedido.fk_pedido_id)
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .filter(
                ProcessamentoPedido.status_processamento == 1,
                Pedido.periodicidade == 2,
                db.func.month(ProcessamentoPedido.data_processamento)
                == get_current_time().month,
                db.func.year(ProcessamentoPedido.data_processamento)
                == get_current_time().year,
            )
            .first()
        )

        return query_quant

    def __get_donations_recurrence_made(self):

        filter_metodo: int = self.__data.get("forma_pagamento")
        filter_campanha: str = self.__data.get("campanha_id")
        filter_nome: str = self.__data.get("nome")
        data_inicio: str = self.__data.get("data_inicio")
        data_fim: str = self.__data.get("data_fim")
        now = get_current_time()

        query = (
            db.session.query(
                Pedido.id.label("pedido_id"),
                Clifor.id.label("clifor_id"),
                Clifor.nome,
                Clifor.cpf_cnpj,
                Pedido.data_criacao,
                ProcessamentoPedido.data_processamento,
                Pedido.valor_total_pedido,
                Campanha.titulo.label("nome_campanha"),
                Campanha.descricao,
                FormaPagamento.descricao.label("metodo_pagamento"),
            )
            .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
            .join(
                FormaPagamento,
                FormaPagamento.id == Pedido.fk_forma_pagamento_id,
            )
            .join(
                ProcessamentoPedido,
                ProcessamentoPedido.fk_pedido_id == Pedido.id,
            )
            .outerjoin(Campanha, Campanha.id == Pedido.fk_campanha_id)
            .filter(
                Pedido.contabilizar_doacao == 1,
                ProcessamentoPedido.status_processamento == 1,
                Pedido.periodicidade == 2,
                (
                    db.func.cast(
                        ProcessamentoPedido.data_processamento, db.Date
                    )
                    >= db.func.cast(data_inicio, db.Date)
                    if data_inicio
                    else True
                ),
                (
                    db.func.cast(
                        ProcessamentoPedido.data_processamento, db.Date
                    )
                    <= db.func.cast(data_fim, db.Date)
                    if data_fim
                    else True
                ),
                (
                    Clifor.nome.ilike(f"%{filter_nome}%")
                    if filter_nome
                    else True
                ),
                (Campanha.id == filter_campanha if filter_campanha else True),
                (
                    FormaPagamento.id == filter_metodo
                    if filter_metodo
                    else True
                ),
                db.func.month(ProcessamentoPedido.data_processamento)
                == now.month,
                db.func.year(ProcessamentoPedido.data_processamento)
                == now.year,
            )
            .order_by(db.desc(ProcessamentoPedido.data_processamento))
        )

        paginate = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        
        if query is None:
            res = []
        else:

            res = [
                {
                    "pedido_id": donation.pedido_id,
                    "clifor_id": donation.clifor_id,
                    "nome": donation.nome,
                    "data_donation": donation.data_processamento.strftime(
                        "%d/%m/%Y"
                    ),
                    "valor": str(round(donation.valor_total_pedido, 2)),
                    "metodo_pagamento": donation.metodo_pagamento,
                    "campanha": donation.nome_campanha,
                }
                for donation in paginate.items
            ]

        pagination_info = {
            "current_page": paginate.page,
            "total_items": paginate.total,
            "per_page": self.__per_page,
        }

        quantidade, total_sum = self.__query_total_and_quant_recurrence()

        info_card = {
            "valor_total": str(round(total_sum, 2)) if total_sum else 0,
            "total_items": quantidade,
        }

        response = {
            "lista": res,
            "pagination": pagination_info,
            "info_card": info_card,
        }

        return response, 200
