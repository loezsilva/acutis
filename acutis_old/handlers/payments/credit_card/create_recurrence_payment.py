from datetime import date, datetime
import logging
import uuid
from flask import jsonify, request
from flask_jwt_extended import current_user
import xmltodict
import requests
from config import MAXIPAGO_URL_XML
from exceptions.exception_mercado_pago import MercadoPagoException
from models.campanha import Campanha
from models.clifor import Clifor
from models.endereco import Endereco
from models.gateway_pagamento import GatewayPagamento
from services.mercado_pago_api import MercadoPago
from utils.checkout import register_order
from utils.functions import send_thanks_for_donation
from utils.logs_access import log_access
from builder import db, translator
from utils.regex import format_string
from utils.validator import cpf_cnpj_validator


class CreateCreditCardRecurrencePayment:
    def __init__(self, payment_setup_id: int) -> None:
        self.__payment_setup = payment_setup_id

    def execute(self):
        METHODS_MAP = {
            1: self.__maxi_pago_recurrence_payment,
            2: self.__mercado_pago_recurrence_payment,
        }

        payment_gateway = METHODS_MAP[self.__payment_setup]
        return payment_gateway()

    def __maxi_pago_recurrence_payment(self):
        try:
            payload = request.get_json()

            numero_cartao = payload["numero_cartao"].strip()
            validade_cartao_mes = payload["validade_cartao_mes"].strip()
            validade_cartao_ano = payload["validade_cartao_ano"].strip()
            codigo_seguranca_cartao = payload[
                "codigo_seguranca_cartao"
            ].strip()
            valor_doacao = payload["valor_doacao"]
            if float(valor_doacao) < 10:
                return {
                    "error": "O valor mínimo a ser doado é de 10 reais."
                }, 400
            campanha_id = payload["fk_campanha_id"]

        except KeyError as err:
            response = {"error": f"O campo {str(err)} é obrigatório."}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return jsonify(response), 400

        campanha = db.session.get(Campanha, campanha_id)
        if not campanha:
            response = {
                "error": f"Campanha com id {campanha_id} não encontrada."
            }
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 404

        gateway_pagamento = GatewayPagamento.query.filter_by(
            fk_empresa_id=campanha.fk_empresa_id
        ).first()
        if not gateway_pagamento:
            response = {"error": f"Gateway de pagamento não encontrado."}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 404

        clifor = db.session.get(Clifor, current_user["fk_clifor_id"])

        endereco = Endereco.query.filter_by(
            fk_clifor_id=current_user["fk_clifor_id"]
        ).first()
        if not endereco:
            response = {"error", f"Endereço não encontrado."}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 404

        url = MAXIPAGO_URL_XML
        headers = {"Content-Type": "text/xml"}

        reference_num = (
            f"{current_user['id']}_CARTAO_{datetime.timestamp(datetime.now())}"
        )

        card_recurrent_transaction_xml = f"""
            <transaction-request>
                <version>3.1.1.15</version>
                <verification>
                    <merchantId>{gateway_pagamento.merchant_id}</merchantId>
                    <merchantKey>{gateway_pagamento.merchant_key}</merchantKey>
                </verification>
                <order>
                    <recurringPayment>
                        <processorID>2</processorID>
                        <referenceNum>{reference_num}</referenceNum>
                        <ipAddress>{request.remote_addr}</ipAddress>
                        <customerIdExt>{clifor.cpf_cnpj}</customerIdExt>
                        <billing>
                            <name>{current_user["nome"]}</name>
                            <address>{format_string(endereco.rua, lower=False)}</address>
                            <address2>{format_string(endereco.complemento, lower=False)}</address2>
                            <district>{format_string(endereco.bairro, lower=False)}</district>
                            <city>{format_string(endereco.cidade, lower=False)}</city>
                            <state>{format_string(endereco.estado, lower=False)}</state>
                            <postalcode>{endereco.cep}</postalcode>
                            <country>BR</country>
                            <phone>{clifor.telefone1}</phone>
                            <email>{current_user["email"]}</email>
                            <companyName>maxiPago!</companyName>
                        </billing>
                        <shipping>
                            <name>{current_user["nome"]}</name>
                            <address>{format_string(endereco.rua, lower=False)}</address>
                            <address2>{format_string(endereco.complemento, lower=False)}</address2>
                            <district>{format_string(endereco.bairro, lower=False)}</district>
                            <city>{format_string(endereco.cidade, lower=False)}</city>
                            <state>{format_string(endereco.estado, lower=False)}</state>
                            <postalcode>{endereco.cep}</postalcode>
                            <country>BR</country>
                            <phone>{clifor.telefone1}</phone>
                            <email>{current_user["email"]}</email>
                        </shipping>
                        <transactionDetail>
                            <payType>
                                <creditCard>
                                    <number>{format_string(numero_cartao, only_digits=True)}</number>
                                    <expMonth>{validade_cartao_mes}</expMonth>
                                    <expYear>20{validade_cartao_ano}</expYear>
                                    <cvvNumber>{codigo_seguranca_cartao}</cvvNumber>
                                </creditCard>
                            </payType>
                        </transactionDetail>
                        <payment>
                            <chargeTotal>{valor_doacao}</chargeTotal>
                            <currencyCode>BRL</currencyCode>
                        </payment>
                        <recurring>
                            <action>new</action>
                            <startDate>{date.today()}</startDate>
                            <period>monthly</period>
                            <frequency>1</frequency>
                            <installments>infinite</installments>
                            <failureThreshold>3</failureThreshold>
                            <onFailureAction>skip</onFailureAction>
                        </recurring>
                    </recurringPayment>
                </order>
            </transaction-request>
        """

        response = requests.post(
            url, data=card_recurrent_transaction_xml, headers=headers
        )

        if not str(response.status_code).startswith("2"):
            logging.error(
                "Error %s: %s" % (response.status_code, response.reason)
            )
            response = {"error": "Ocorreu uma falha ao efetuar o pagamento."}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 500

        response = xmltodict.parse(response.text)

        try:
            transaction = response["transaction-response"]

            order_id = transaction.get("orderID")
            transaction_id = transaction.get("transactionID")
            processor_message = transaction.get("processorMessage")
            response_code = int(transaction["responseCode"])
            response_message = transaction["responseMessage"]
            status_processamento = 0

            if response_code == 0:
                if response_message == "CAPTURED":
                    status_processamento = 1
                vencimento_cartao = "/".join(
                    [validade_cartao_mes, validade_cartao_ano]
                )
                register_order(
                    campanha=campanha,
                    clifor=clifor,
                    reference_num=reference_num,
                    valor_doacao=valor_doacao,
                    forma_pagamento=1,
                    periodo=2,
                    id_pedido=order_id,
                    id_transacao=transaction_id,
                    fk_gateway_pagamento_id=self.__payment_setup,
                    vencimento_cartao=vencimento_cartao,
                    status_processamento=status_processamento,
                )

                send_thanks_for_donation(
                    campanha, current_user["nome"], current_user["email"]
                )

                response = {
                    "id_pedido": order_id,
                    "id_transacao": transaction_id,
                    "response_code": response_code,
                    "numero_referencia": reference_num,
                    "processor_message": processor_message,
                    "msg": "Transação autorizada.",
                }, 200
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response

            response = {
                "id_pedido": order_id,
                "id_transacao": transaction_id,
                "response_code": response_code,
                "numero_referencia": reference_num,
                "processor_message": processor_message,
                "error": "Transação não autorizada, revise suas informações de pagamento.",
            }, 400
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

        except KeyError as err:
            logging.error(f"{type(err)} - {err}")
            response = {
                "error": "Ocorreu uma falha ao efetuar o pagamento."
            }, 500
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

        except Exception as err:
            response = {"error": str(err)}, 500
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

    def __mercado_pago_recurrence_payment(self):
        try:
            payload = request.get_json()

            numero_cartao = format_string(
                payload["numero_cartao"].strip(), only_digits=True
            )
            validade_cartao_mes = payload["validade_cartao_mes"].strip()
            validade_cartao_ano = payload["validade_cartao_ano"].strip()
            codigo_seguranca_cartao = payload[
                "codigo_seguranca_cartao"
            ].strip()
            nome_titular_cartao = payload["nome_titular_cartao"].strip()
            cpf_cnpj_titular_cartao = cpf_cnpj_validator(
                payload["cpf_cnpj_titular_cartao"].strip()
            )
            valor_doacao = payload["valor_doacao"]
            if float(valor_doacao) < 10:
                return {
                    "error": "O valor mínimo a ser doado é de 10 reais."
                }, 400
            fk_campanha_id = payload["fk_campanha_id"]
            device_id = payload["device_id"]

            email = current_user["email"]

            reference_num = f"{current_user['id']}_CARTAO_MPAG_{datetime.timestamp(datetime.now())}"

            clifor = db.session.get(Clifor, current_user["fk_clifor_id"])

            if (campanha := db.session.get(Campanha, fk_campanha_id)) is None:
                response = {"error": "Campanha não encontrada."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 404

            card_token_request = {
                "card_number": numero_cartao,
                "cardholder": {
                    "name": nome_titular_cartao,
                    "identification": {
                        "type": (
                            "CPF"
                            if len(cpf_cnpj_titular_cartao) == 11
                            else "CNPJ"
                        ),
                        "number": cpf_cnpj_titular_cartao,
                    },
                },
                "expiration_year": f"20{validade_cartao_ano}",
                "expiration_month": validade_cartao_mes,
                "security_code": codigo_seguranca_cartao,
            }

            mp = MercadoPago()
            card_token = mp.create_card_token(card_token_request)

            payment_data = {
                "auto_recurring": {
                    "frequency": 1,
                    "frequency_type": "months",
                    "transaction_amount": float(valor_doacao),
                    "currency_id": "BRL",
                },
                "back_url": "https://doe.institutohesed.org.br/",
                "card_token_id": card_token.get("id"),
                "external_reference": str(uuid.uuid4()),
                "payer_email": email,
                "reason": f"Doação recorrente para a campanha {campanha.titulo}",
                "status": "authorized",
            }

            response_mp = mp.create_recurrence_payment(payment_data, device_id)

            if response_mp.get("status") != "authorized":
                response = {
                    "error": "Ocorreu um erro ao realizar a doação. Tente novamente mais tarde!",
                    "msg_error": response_mp,
                }
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 500

            vencimento_cartao = "/".join(
                [validade_cartao_mes, validade_cartao_ano]
            )
            register_order(
                campanha=campanha,
                clifor=clifor,
                reference_num=reference_num,
                valor_doacao=valor_doacao,
                forma_pagamento=1,
                periodo=2,
                id_pedido=response_mp.get("id"),
                id_transacao=response_mp.get("id"),
                vencimento_cartao=vencimento_cartao,
                status_processamento=1,
                fk_gateway_pagamento_id=self.__payment_setup,
                create_transaction=False,
            )

            log_access(
                response_mp,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )

            return jsonify({"msg": "Pronto, seu pagamento foi aprovado!"}), 201

        except MercadoPagoException as mp_exception:
            error = translator.translate(mp_exception.error_message)
            return {"error": error}, mp_exception.status_code

        except Exception as err:
            response = {
                "error": "Ocorreu um erro ao realizar a doação. Tente novamente mais tarde!",
                "msg_error": str(err),
                "type_error": str(type(err)),
            }
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 500
