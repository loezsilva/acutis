from http import HTTPStatus
from models import Pedido, Clifor, Campanha, FormaPagamento, Usuario
from builder import db
from flask import request

from models.schemas.checkout.get.listar_recorrencias_canceladas import (
    ListarRecorrenciasCanceladasQuery,
)
from repositories.interfaces.checkout_repository_interface import (
    CheckoutRepositoryInterface,
)

class ListarRecorrenciasCanceladas:
    def __init__(self, checkout_repository: CheckoutRepositoryInterface) -> None:
        self.__checkout_repository = checkout_repository

    def execute(self):
        filtros = ListarRecorrenciasCanceladasQuery.parse_obj(request.args)
        recorrencias_canceladas, informacoes_para_card = (
            self.__checkout_repository.get_listar_recorrencias_canceladas(filtros)
        )
        return self.__formatar_resposta(recorrencias_canceladas, informacoes_para_card)

    def __formatar_resposta(
        self, listagem: tuple, informacoes_adicionais: tuple
    ) -> tuple[dict, HTTPStatus]:

        total_canceladas, valor_total_canceladas = informacoes_adicionais[0]

        response = {
            "page": listagem.page,
            "pages": listagem.pages,
            "total": listagem.total,
            "card_qtd_doacoes": total_canceladas,
            "card_soma_valor_doacoes": str(round(valor_total_canceladas, 2)),
            "doacoes_recorrentes_canceladas": [
                {
                    "id": doacao.id,
                    "benfeitor": doacao.nome,
                    "campanha": doacao.titulo,
                    "data_pedido": doacao.data_pedido.strftime("%d/%m/%Y %H:%M:%S"),
                    "metodo": doacao.metodo_pagamento,
                    "valor": str(round(doacao.valor_total_pedido, 2)),
                    "cancelada_em": (
                        doacao.cancelada_em.strftime("%d/%m/%Y %H:%M:%S")
                        if doacao.cancelada_em
                        else None
                    ),
                    "cancelada_por": (
                        self.__checkout_repository.get_informacoes_sobre_usuario(
                            doacao.cancelada_por
                        ).nome
                        if doacao.cancelada_por != None
                        else None
                    ),
                }
                for doacao in listagem.items
            ],
        }

        return response, HTTPStatus.OK
