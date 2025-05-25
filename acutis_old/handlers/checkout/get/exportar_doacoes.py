from http import HTTPStatus
from flask import request
from models.schemas.checkout.get.listar_doacoes_schema import ListarDoacoesQuery
from repositories.interfaces.checkout_repository_interface import (
    CheckoutRepositoryInterface,
)
from utils.export_excel import export_excel
from datetime import datetime


class ExportarDoacoes:
    def __init__(self, checkout_repository: CheckoutRepositoryInterface) -> None:
        self.__checkout_repository = checkout_repository

    def execute(self):
        filtros = ListarDoacoesQuery.parse_obj(request.args)
        donations = self.__checkout_repository.exportar_doacoes(
            filtros
        )
        return self.__formatar_resposta(donations)

    def __formatar_resposta(self, donations_query: tuple) -> tuple:

        STATUS_PROCESSAMENTO_MAP = {
            0: "Em processamento",
            1: "Pago",
            2: "Não efetuado",
            3: "Expirado",
        }

        res = [
            {
                "Pedido_id": donation.fk_pedido_id,
                "Método": donation.forma_pagamento,
                "Código_referêncial": donation.id_transacao_gateway,
                "Comprovante_id": donation.id_pagamento,
                "Transação_id": donation.transaction_id,
                "Nome": donation.nome,
                "CPF/CNPJ": donation.cpf_cnpj,
                "Data": donation.data_processamento.strftime("%d-%m-%Y %H:%M:%S"),
                "Valor": round(donation.valor_total_pedido, 2),
                "Status": STATUS_PROCESSAMENTO_MAP.get(
                    donation.status_processamento, "Desconhecido"
                ),
                "Gateway": donation.gateway_pagamento_nome,
                "Campanha": donation.titulo,
            }
            for donation in donations_query
        ]

        return export_excel(res, "doacoes"), HTTPStatus.OK
