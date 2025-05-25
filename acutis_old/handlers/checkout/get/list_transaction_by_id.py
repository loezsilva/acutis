from flask_jwt_extended import current_user
from exceptions.error_types.http_not_found import NotFoundError
from builder import db
import math
from flask import request
from models import ProcessamentoPedido, FormaPagamento, Pedido
from models.perfil import ProfilesEnum


class ListTransactionById:
    def __init__(self, fk_pedido_id: int) -> None:
        self.__args = request.args
        self.__per_page = self.__args.get("per_page", 10, type=int)
        self.__page = self.__args.get("page", 1, type=int)
        self.__fk_pedido_id = fk_pedido_id

        self.__transaction_id = self.__args.get("transaction_id")
        self.__data_inicial = self.__args.get("data_inicial")
        self.__data_final = self.__args.get("data_final")
        self.__status = self.__args.get("status")
        self.__metodo = self.__args.get("metodo")

    def execute(self) -> None:
        transaction = self.__query()
        return self.__format_response(transaction)

    def __query(self) -> None:

        pedido_query = Pedido.query.filter(Pedido.id == self.__fk_pedido_id)

        if (
            str(current_user["nome_perfil"]).lower()
            == ProfilesEnum.GESTOR_DOACOES.lower()
        ):
            pedido_query = pedido_query.filter(Pedido.anonimo == False)

        pedido = pedido_query.scalar()

        if pedido is None:
            raise NotFoundError("Pedido não encontrado")

        transacoes_query = (
            db.session.query(
                ProcessamentoPedido.id,
                ProcessamentoPedido.transaction_id,
                ProcessamentoPedido.data_processamento.label("data"),
                ProcessamentoPedido.valor,
                ProcessamentoPedido.status_processamento.label("status"),
                FormaPagamento.descricao.label("metodo"),
            )
            .join(
                FormaPagamento,
                FormaPagamento.id == ProcessamentoPedido.fk_forma_pagamento_id,
            )
            .filter(
                (
                    ProcessamentoPedido.transaction_id == self.__transaction_id
                    if self.__transaction_id
                    else True
                ),
                (
                    db.and_(
                        db.cast(
                            ProcessamentoPedido.data_processamento, db.Date
                        )
                        >= self.__data_inicial,
                        db.cast(
                            ProcessamentoPedido.data_processamento, db.Date
                        )
                        <= self.__data_final,
                    )
                    if self.__data_inicial
                    else True
                ),
                (
                    ProcessamentoPedido.status_processamento == self.__status
                    if self.__status
                    else True
                ),
                (
                    ProcessamentoPedido.fk_forma_pagamento_id == self.__metodo
                    if self.__metodo
                    else True
                ),
                ProcessamentoPedido.fk_pedido_id == self.__fk_pedido_id,
            )
            .order_by(ProcessamentoPedido.data_processamento.desc())
        )

        transacoes_paginate = transacoes_query.paginate(
            page=self.__page, per_page=self.__per_page, error_out=False
        )

        return transacoes_paginate

    def __format_response(self, data: tuple) -> tuple:

        response = {
            "page": self.__page,
            "pages": math.ceil(data.total / self.__per_page),
            "total": data.total,
            "transacoes": [
                {
                    "id": transacao.id,
                    "transaction_id": transacao.transaction_id,
                    "data": transacao.data.strftime("%d/%m/%Y %H:%M:%S"),
                    "valor": str(round(transacao.valor, 2)),
                    "status": transacao.status,
                    "metodo": transacao.metodo,
                }
                for transacao in data
            ],
        }

        return response, 200
