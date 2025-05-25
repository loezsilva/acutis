from datetime import datetime
from logging import Logger
from typing import Dict, List

from flask import request as FlaskRequest

from models.campanha import Campanha
from models.clifor import Clifor
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from services.itau_api import ItauAPI
from builder import db
from utils.functions import get_current_time, send_thanks_for_donation


class ItauWebhook:
    def __init__(self, logger: Logger) -> None:
        self.logger = logger

    def execute(self, request: FlaskRequest):  # type: ignore
        try:
            body = request.json
            data = body["pix"][0]

            return self.__register_donation(data)

        except Exception as err:
            db.session.rollback()
            self.logger.error(
                {
                    "error": "Ocorreu um erro ao salvar o pagamento no Itau Webhook.",
                    "errorMsg": f"{str(type(err))} - {str(err)}",
                    "requisicao": data,
                }
            )
            return {}, 500

    def __register_donation(self, data: List[Dict]):
        anon_donation = data[
            "componentesValor"
        ]  # Se não existir o campo "original" dentro de "componentesValor", a doação é anonima.
        if anon_donation in [None, "None"]:
            return self.__register_anonymous_donation_data(data)

        return self.__register_acutis_user_donation(data)

    def __register_anonymous_donation_data(self, data: List[Dict]):
        id_pagamento = data["endToEndId"]
        chave_pix = data["chave"]

        itau = ItauAPI("bolecode")
        path = "/lancamentos_pix"
        params = {"e2eid": id_pagamento, "chaves": chave_pix}

        response, status = itau.get(path, params)
        if status != 200:
            self.logger.error(
                {
                    "error": "Pagamento não encontrado.",
                    "requisicao anonima": data,
                }
            )
            return {}, 200

        payload = response["data"]
        if len(payload) == 0:
            self.logger.error(
                {
                    "error": "Pagamento ainda não registrado na API do Itau.",
                    "requisicao": response,
                }
            )
            return {}, 500
        payload = payload[0]

        payload_usuario = payload["detalhe_pagamento"]["debitado"]
        payload_pagamento = payload["detalhe_pagamento"]
        payload_valor = payload["detalhe_pagamento"]["detalhe_valor"]

        cpf_cnpj = payload_usuario["numero_documento"]
        nome = payload_usuario["nome"]
        data_pagamento = payload_pagamento["data"]
        valor_pagamento = payload_valor["valor"]
        txid = payload["detalhe_pagamento"].get("id_lancamento", None)

        clifor = Clifor.query.filter_by(cpf_cnpj=cpf_cnpj).first()
        if clifor and clifor.fk_usuario_id is not None:
            reference_num = f"{clifor.fk_usuario_id}_PIX_{datetime.timestamp(datetime.now())}"
        else:
            reference_num = f"0_PIX_{datetime.timestamp(datetime.now())}"

        campanha = Campanha.query.filter_by(chave_pix=chave_pix).first()

        if not clifor:
            MAP_CPF_CNPJ = {11: "f", 14: "j"}

            clifor = Clifor(
                fk_empresa_id=1,
                tipo_clifor=MAP_CPF_CNPJ[len(cpf_cnpj)],
                nome=nome,
                cpf_cnpj=cpf_cnpj,
            )

            db.session.add(clifor)
            db.session.flush()

        pedido = Pedido(
            fk_empresa_id=1,
            fk_clifor_id=clifor.id,
            fk_campanha_id=campanha.id if campanha else None,
            fk_forma_pagamento_id=2,
            data_pedido=data_pagamento,
            periodicidade=1,
            status_pedido=1,
            valor_total_pedido=valor_pagamento,
            anonimo=True,
            recorrencia_ativa=False,
            usuario_criacao=0,
            fk_gateway_pagamento_id=1,
        )

        db.session.add(pedido)
        db.session.flush()

        processamento_pedido = ProcessamentoPedido(
            fk_empresa_id=1,
            fk_pedido_id=pedido.id,
            fk_clifor_id=clifor.id,
            fk_forma_pagamento_id=2,
            data_processamento=data_pagamento,
            valor=valor_pagamento,
            status_processamento=1,
            id_transacao_gateway=reference_num,
            transaction_id=txid,
            id_pagamento=id_pagamento,
            usuario_criacao=0,
        )

        db.session.add(processamento_pedido)

        db.session.commit()

        return {}, 200

    def __register_acutis_user_donation(self, data: List[Dict]):
        txid = data["txid"]
        id_pagamento = data["endToEndId"]

        pagamento_ja_cadastrado = ProcessamentoPedido.query.filter_by(
            id_pagamento=id_pagamento
        ).first()
        if pagamento_ja_cadastrado:
            return {}, 200

        processamento_pedido = ProcessamentoPedido.query.filter_by(
            transaction_id=txid
        ).first()
        if not processamento_pedido:
            self.logger.error(
                {
                    "error": "Pedido não encontrado.",
                    "requisicao usuario acutis": data,
                }
            )
            return {}, 200

        pedido = db.session.get(Pedido, processamento_pedido.fk_pedido_id)
        clifor = db.session.get(Clifor, pedido.fk_clifor_id)
        campanha = db.session.get(Campanha, pedido.fk_campanha_id)

        processamento_pedido.status_processamento = 1
        processamento_pedido.id_pagamento = id_pagamento
        processamento_pedido.data_processamento = get_current_time()

        db.session.commit()

        send_thanks_for_donation(campanha, clifor.nome, clifor.email)

        return {}, 200
