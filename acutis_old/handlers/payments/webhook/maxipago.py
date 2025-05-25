import logging
from flask import request
import xmltodict

from models.campanha import Campanha
from models.clifor import Clifor
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from builder import db
from utils.functions import get_current_time, send_thanks_for_donation


class MaxiPagoWebhook:
    def __init__(self, logger) -> None:
        self.logger = logger

    def execute(self):
        return self.__get_data()

    def __get_data(self):
        try:
            xml_data = request.get_data(as_text=True)
            print(f"XML_DATA_AS_TEXT: {xml_data}")
            logging.error(f"XML_DATA_AS_TEXT: {xml_data}")

            if xml_data.startswith("xml=") or xml_data.startswith("<?xml"):
                xml_data = xml_data[xml_data.find("<Request>") :]

            response = xmltodict.parse(xml_data)
            print(f"XML_DATA_PARSED: {response}")
            logging.error(f"XML_DATA_PARSED: {response}")

            data = response["Request"]["transaction-event"]
            order_id = data["orderID"]
            reference_num = data["referenceNumber"]
            valor_doacao = data["transactionAmount"]
            transaction_id = data["transactionID"]
            data_processamento = get_current_time()

            if (
                ProcessamentoPedido.query.filter_by(
                    transaction_id=transaction_id
                ).first()
                is not None
            ):
                self.logger.error(
                    {
                        "error": "Pagamento ja registrado.",
                        "requisicao": response,
                        "headers": request.headers,
                    }
                )
                return {}, 200

            if (
                pedido := Pedido.query.filter_by(order_id=order_id).first()
            ) is None:
                self.logger.error(
                    {
                        "error": "Pedido nao encontrado.",
                        "requisicao": response,
                        "headers": request.headers,
                    }
                )
                return {}, 200

            processamento_pedido = ProcessamentoPedido.query.filter_by(
                id_transacao_gateway=reference_num, fk_pedido_id=pedido.id
            ).first()

            clifor = db.session.get(Clifor, pedido.fk_clifor_id)
            campanha = db.session.get(Campanha, pedido.fk_campanha_id)

            status_processamento = (
                1 if data["transactionState"] == "Captured" else 2
            )

            novo_processamento_pedido = ProcessamentoPedido(
                fk_empresa_id=processamento_pedido.fk_empresa_id,
                fk_filial_id=processamento_pedido.fk_filial_id,
                fk_pedido_id=processamento_pedido.fk_pedido_id,
                fk_clifor_id=processamento_pedido.fk_clifor_id,
                fk_forma_pagamento_id=processamento_pedido.fk_forma_pagamento_id,
                data_processamento=data_processamento,
                valor=float(valor_doacao),
                status_processamento=status_processamento,
                id_transacao_gateway=processamento_pedido.id_transacao_gateway,
                transaction_id=transaction_id,
                usuario_criacao=processamento_pedido.usuario_criacao,
            )

            db.session.add(novo_processamento_pedido)
            db.session.commit()

            if status_processamento == 1:
                send_thanks_for_donation(campanha, clifor.nome, clifor.email)

            self.logger.info("Sucesso ao salvar os dados do webhook maxipago")
            return {}, 200

        except Exception as err:
            db.session.rollback()
            self.logger.error(
                {
                    "error": "Ocorreu um erro ao salvar o pagamento.",
                    "errorMsg": f"{str(type(err))} - {str(err)}",
                    "requisicao": response,
                    "headers": request.headers,
                }
            )
            return {}, 500
