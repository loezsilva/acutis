from http import HTTPStatus
from flask import request
from exceptions.error_types.http_bad_request import BadRequestError
from models.schemas.checkout.get.listar_doacoes_schema import ListarDoacoesQuery
from repositories.interfaces.checkout_repository_interface import CheckoutRepositoryInterface

class ListaTodasDoacoes:

    def __init__(self, checkout_repository: CheckoutRepositoryInterface) -> None:
        self.__checkout_repository = checkout_repository
        
    def execute(self):
        filtros = ListarDoacoesQuery.parse_obj(request.args)
        doacoes, valor_total = self.__checkout_repository.get_listagem_de_doacoes(filtros)
        return self.__formatar_resposta(doacoes, valor_total)

    def __formatar_resposta(self, data: tuple, valor_total) -> tuple:

        STATUS_PROCESSAMENTO_MAP = {
            0: "Em processamento",
            1: "Pago",
            2: "Não efetuado",
        }

        resposta = {
            "total_doado": str(round(valor_total, 2)),
            "page": data.page,
            "pages": data.pages,
            "total": data.total,
            "data": [
                {
                    "benfeitor": {
                        "deleted_at": (
                            doacoes.deleted_at.strftime("%d/%m/%Y %H:%M:%S")
                            if doacoes.deleted_at
                            else None
                        ),
                        "user_id": doacoes.fk_usuario_id,
                        "fk_clifor_id": doacoes.id,
                        "nome": (
                            "----"
                            if doacoes.fk_gateway_pagamento_id == 2
                            and doacoes.fk_usuario_id is None
                            else doacoes.nome
                        ),
                    },
                    "campanha": {
                        "descricao": doacoes.descricao,
                        "fk_campanha_id": doacoes.fk_campanha_id,
                        "imagem": doacoes.filename,
                        "titulo": doacoes.titulo,
                    },
                    "pedido": {
                        "cancelada_por": self.__checkout_repository.get_informacoes_sobre_usuario(doacoes.cancelada_por).nome if doacoes.cancelada_por != None else None,
                        "anonimo": doacoes.anonimo,
                        "data_doacao": (
                            doacoes.data_processamento.strftime(
                                "%d/%m/%Y %H:%M:%S"
                            )
                            if doacoes.data_processamento
                            else None
                        ),
                        "fk_pedido_id": doacoes.fk_pedido_id,
                        "forma_pagamento": doacoes.forma_pagamento,
                        "recorrencia": (
                            True if doacoes.periodicidade == 2 else False
                        ),
                        "recorrencia_ativa": doacoes.recorrencia_ativa,
                        "cancelada_em": (
                            doacoes.cancelada_em.strftime("%d/%m/%Y %H:%M:%S")
                            if doacoes.cancelada_em
                            else None
                        ),
                        "order_id": doacoes.order_id,
                        "valor_doacao": str(
                            round(doacoes.valor_total_pedido, 2)
                        ),
                        "contabilizar_doacao": doacoes.contabilizar_doacao,
                        "status_pedido": doacoes.status_pedido,
                        "gateway_pagamento": {
                            "id": doacoes.fk_gateway_pagamento_id,
                            "nome": doacoes.gateway_pagamento_nome,
                        },
                    },
                    "processamento": {
                        "codigo_referencia": doacoes.id_transacao_gateway,
                        "fk_processamento_pedido_id": doacoes.fk_processamento_pedido_id,
                        "status": STATUS_PROCESSAMENTO_MAP[
                            doacoes.status_processamento
                        ],
                        "transaction_id": doacoes.transaction_id,
                        "id_pagamento": doacoes.id_pagamento,
                    },
                }
                for doacoes in data
            ],
        }

        return resposta, HTTPStatus.OK
