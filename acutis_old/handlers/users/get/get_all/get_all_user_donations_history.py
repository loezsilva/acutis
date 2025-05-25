from flask import request
from flask_jwt_extended import current_user
from flask_sqlalchemy import SQLAlchemy

from exceptions.error_types.http_not_found import NotFoundError
from models.forma_pagamento import FormaPagamento
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido


class GetAllUserDonationsHistory:
    def __init__(self, database: SQLAlchemy) -> None:
        self.__database = database
        self.__page = request.args.get("page", 1, type=int)
        self.__per_page = request.args.get("per_page", 10, type=int)
        self.__STATUS_PROCESSAMENTO = {
            0: "Em processamento",
            1: "Pago",
            2: "Não efetuado",
        }

    def execute(self, fk_pedido_id: int):
        clifor_id = current_user["fk_clifor_id"]

        self.__validate_donation_permission(fk_pedido_id, clifor_id)
        historico_doacoes_query = self.__get_all_user_donations_history_query(
            fk_pedido_id
        )
        historico_doacoes, total = self.__paginate_query(historico_doacoes_query)
        response = self.__prepare_response(historico_doacoes, total)
        return response, 200

    def __validate_donation_permission(self, fk_pedido_id: int, clifor_id: int) -> None:
        pedido: Pedido = self.__database.session.get(Pedido, fk_pedido_id)
        if pedido is None or pedido.fk_clifor_id != clifor_id:
            raise NotFoundError("Esta doação não foi encontrada entre suas doações.")

    def __get_all_user_donations_history_query(self, fk_pedido_id: int):
        historico_doacoes_query = (
            self.__database.session.query(
                ProcessamentoPedido.data_criacao.label("data_doacao"),
                ProcessamentoPedido.valor.label("valor_doacao"),
                FormaPagamento.descricao.label("forma_pagamento"),
                ProcessamentoPedido.status_processamento,
            )
            .join(
                FormaPagamento,
                FormaPagamento.id == ProcessamentoPedido.fk_forma_pagamento_id,
            )
            .filter(ProcessamentoPedido.fk_pedido_id == fk_pedido_id)
            .order_by(ProcessamentoPedido.data_criacao.desc())
        )

        return historico_doacoes_query

    def __paginate_query(self, query):
        query_pagination = query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )
        items, total = query_pagination.items, query_pagination.total
        return items, total

    def __prepare_response(
        self, historico_doacoes: list[ProcessamentoPedido], total: int
    ) -> dict:
        response = {
            "page": self.__page,
            "total": total,
            "historico_doacoes": [
                {
                    "data_doacao": (
                        doacao.data_doacao.strftime("%d/%m/%Y")
                        if doacao.data_doacao
                        else None
                    ),
                    "valor_doacao": round(doacao.valor_doacao, 2),
                    "forma_pagamento": doacao.forma_pagamento,
                    "status_processamento": self.__STATUS_PROCESSAMENTO[
                        doacao.status_processamento
                    ],
                }
                for doacao in historico_doacoes
            ],
        }

        return response
