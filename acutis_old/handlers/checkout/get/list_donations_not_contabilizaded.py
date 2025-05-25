from builder import db
from models import (
    Usuario,
    Clifor,
    Pedido,
    Campanha,
    ProcessamentoPedido,
    FormaPagamento,
    GatewayPagamento,
)
import math
from exceptions.errors_handler import errors_handler
from flask import request


class DonationsNotContabilizaded:
    def __init__(self) -> None:
        self.__data = request.args

        self.__per_page = self.__data.get("per_page", 10, type=int)
        self.__page = self.__data.get("page", 1, type=int)

    def execute(self):
        donations = self.__query_donations_not_contabilizaded()
        return self.__format_response(donations)

    def __query_donations_not_contabilizaded(self):
        try:
            selected_columns = [
                Usuario.deleted_at,
                Pedido.anonimo,
                Clifor.id,
                Clifor.nome,
                Clifor.fk_usuario_id,
                Campanha.descricao,
                Campanha.id.label("fk_campanha_id"),
                Campanha.filename,
                Campanha.titulo,
                ProcessamentoPedido.data_processamento,
                FormaPagamento.descricao.label("forma_pagamento"),
                Pedido.id.label("fk_pedido_id"),
                Pedido.order_id,
                ProcessamentoPedido.id_transacao_gateway,
                ProcessamentoPedido.id.label("fk_processamento_pedido_id"),
                ProcessamentoPedido.status_processamento,
                ProcessamentoPedido.transaction_id,
                Pedido.periodicidade,
                Pedido.recorrencia_ativa,
                Pedido.valor_total_pedido,
                Pedido.contabilizar_doacao,
                Pedido.fk_gateway_pagamento_id,
                Pedido.cancelada_em,
                Pedido.status_pedido,
                GatewayPagamento.descricao.label("gateway_pagamento_nome"),
            ]

            query_donations = (
                db.session.query(*selected_columns)
                .select_from(Pedido)
                .join(
                    ProcessamentoPedido,
                    Pedido.id == ProcessamentoPedido.fk_pedido_id,
                )
                .join(
                    FormaPagamento,
                    Pedido.fk_forma_pagamento_id == FormaPagamento.id,
                )
                .join(
                    Campanha,
                    Pedido.fk_campanha_id == Campanha.id,
                    isouter=True,
                )
                .join(Clifor, Clifor.id == Pedido.fk_clifor_id)
                .join(
                    Usuario, Clifor.fk_usuario_id == Usuario.id, isouter=True
                )
                .join(
                    GatewayPagamento,
                    GatewayPagamento.id == Pedido.fk_gateway_pagamento_id,
                )
                .filter(Pedido.contabilizar_doacao == False)
                .distinct()
                .order_by(ProcessamentoPedido.data_processamento.desc())
            )

            paginate = query_donations.paginate(
                per_page=self.__per_page,  # Número de itens por página
                page=self.__page,  # Número da página atual
                error_out=False,  # Não lançar erro se a página estiver fora do intervalo
            )

            return paginate
        except Exception as err:
            raise errors_handler(err)

    def __format_response(self, data: dict):

        STATUS_PROCESSAMENTO_MAP = {
            0: "Em processamento",
            1: "Pago",
            2: "Não efetuado",
        }

        total = data.total
        donations = data.items

        result = {
            "per_page": self.__per_page,
            "page": self.__page,
            "pages": math.ceil(data.total / self.__per_page),
            "total": total,
            "data": [
                {
                    "benfeitor": {
                        "deleted_at": (
                            str(
                                donation.deleted_at.strftime(
                                    "%d/%m/%Y %H:%M:%S"
                                )
                            )
                            if donation.deleted_at
                            else None
                        ),
                        "user_id": donation.fk_usuario_id,
                        "fk_clifor_id": donation.id,
                        "nome": (
                            "----"
                            if donation.fk_gateway_pagamento_id == 2
                            and donation.fk_usuario_id is None
                            else donation.nome
                        ),
                    },
                    "campanha": {
                        "descricao": donation.descricao,
                        "fk_campanha_id": donation.fk_campanha_id,
                        "imagem": donation.filename,
                        "titulo": donation.titulo,
                    },
                    "pedido": {
                        "anonimo": donation.anonimo,
                        "data_doacao": (
                            str(
                                donation.data_processamento.strftime(
                                    "%d/%m/%Y %H:%M:%S"
                                )
                            )
                            if donation.data_processamento
                            else None
                        ),
                        "fk_pedido_id": donation.fk_pedido_id,
                        "forma_pagamento": donation.forma_pagamento,
                        "recorrencia": (
                            True if donation.periodicidade == 2 else False
                        ),
                        "recorrencia_ativa": donation.recorrencia_ativa,
                        "cancelada_em": str(donation.cancelada_em),
                        "order_id": donation.order_id,
                        "valor_doacao": str(
                            round(donation.valor_total_pedido, 2)
                        ),
                        "contabilizar_doacao": donation.contabilizar_doacao,
                        "status_pedido": donation.status_pedido,
                        "gateway_pagamento": {
                            "id": donation.fk_gateway_pagamento_id,
                            "nome": donation.gateway_pagamento_nome,
                        },
                    },
                    "processamento": {
                        "codigo_referencia": donation.id_transacao_gateway,
                        "fk_processamento_pedido_id": donation.fk_processamento_pedido_id,
                        "status": STATUS_PROCESSAMENTO_MAP[
                            donation.status_processamento
                        ],
                        "transaction_id": donation.transaction_id,
                    },
                }
                for donation in donations
            ],
        }

        return result, 200
