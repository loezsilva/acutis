from datetime import datetime
import logging
import uuid
from flask import request
from flask_jwt_extended import current_user
import requests
import xmltodict

from config import MAXIPAGO_URL_XML
from exceptions.exception_mercado_pago import MercadoPagoException
from models.campanha import Campanha
from models.clifor import Clifor
from models.endereco import Endereco
from models.forma_pagamento import FormaPagamento
from models.gateway_pagamento import GatewayPagamento
from services.mercado_pago_api import MercadoPago
from use_cases.checkout_mp.payment_credit_card.payment_credit_card_use_case import (
    PaymentCreditCardUseCase,
)
from utils.checkout import register_order
from utils.functions import send_thanks_for_donation
from utils.logs_access import log_access
from utils.regex import format_string
from builder import db, translator
from utils.validator import cpf_cnpj_validator


class CreateCreditCardPayment:
    def __init__(self, payment_setup_id: int) -> None:
        self.__payment_setup = payment_setup_id

    def execute(self):
        METHODS_MAP = {
            1: self.__maxi_pago_payment,
            2: self.__mercado_pago_payment,
        }

        payment_gateway = METHODS_MAP[self.__payment_setup]
        return payment_gateway()

    def __maxi_pago_payment(self):
        payload = request.get_json()

        for field, value in payload.items():
            if not value:
                response = {
                    "error": f"O campo {field} não pode estar vazio."
                }, 400
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response

        try:
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
            response = {"error": f"O campo {str(err)} é obrigatório."}, 400
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

        campanha = db.session.get(Campanha, campanha_id)
        if not campanha:
            response = {
                "error": f"Campanha com id {campanha_id} não encontrada."
            }, 404
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

        gateway_pagamento = GatewayPagamento.query.filter_by(
            fk_empresa_id=campanha.fk_empresa_id
        ).first()
        if not gateway_pagamento:
            response = {"error": f"Gateway de pagamento não encontrado."}, 404
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

        clifor = db.session.get(Clifor, current_user["fk_clifor_id"])

        endereco = Endereco.query.filter_by(
            fk_clifor_id=current_user["fk_clifor_id"]
        ).first()
        if not endereco:
            response = {"error", f"Endereço não encontrado."}, 404
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response

        url = MAXIPAGO_URL_XML
        headers = {"Content-Type": "text/xml"}

        reference_num = (
            f"{current_user['id']}_CARTAO_{datetime.timestamp(datetime.now())}"
        )
        forma_pagamento_id = (
            db.session.query(FormaPagamento.id)
            .filter_by(tipo_forma_pagamento=4)
            .first()[0]
        )

        card_transaction_xml = f"""
            <transaction-request>
                <version>3.1.1.15</version>
                <verification>
                    <merchantId>{gateway_pagamento.merchant_id}</merchantId>
                    <merchantKey>{gateway_pagamento.merchant_key}</merchantKey>
                </verification>
                <order>
                    <sale>
                        <processorID>2</processorID>
                        <referenceNum>{reference_num}</referenceNum>
                        <fraudCheck>N</fraudCheck>
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
                    </sale>
                </order>
            </transaction-request>
        """

        response = requests.post(
            url, data=card_transaction_xml, headers=headers
        )

        if not str(response.status_code).startswith("2"):
            logging.error(
                "Error %s: %s" % (response.status_code, response.reason)
            )
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

        response = xmltodict.parse(response.text)

        try:
            transaction = response["transaction-response"]

            order_id = transaction["orderID"]
            transaction_id = transaction["transactionID"]
            processor_message = transaction["processorMessage"]
            response_message = transaction["responseMessage"]
            response_code = int(transaction["responseCode"])
            status_processamento = 0

            if response_code == 0:
                if response_message == "CAPTURED":
                    status_processamento = 1

                register_order(
                    campanha,
                    clifor,
                    reference_num,
                    valor_doacao,
                    forma_pagamento=forma_pagamento_id,
                    periodo=1,
                    id_pedido=order_id,
                    id_transacao=transaction_id,
                    fk_gateway_pagamento_id=self.__payment_setup,
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
                    "msg": "Pagamento efetuado com sucesso.",
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

    def __mercado_pago_payment(self):
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

            cpf_cnpj = current_user["numero_documento"]
            email = current_user["email"]
            nome = current_user["nome"]

            first_name = nome.split(" ")[0]
            last_name = nome.split(" ")[-1]

            tipo_documento = "CPF" if len(cpf_cnpj) == 11 else "CNPJ"

            reference_num = f"{current_user['id']}_CARTAO_MPAG_{datetime.timestamp(datetime.now())}"

            clifor = db.session.get(Clifor, current_user["fk_clifor_id"])

            codigo_area = clifor.telefone1[:3] if clifor.telefone1 else None
            telefone = clifor.telefone1[3:] if clifor.telefone1 else None

            forma_pagamento = (
                db.session.query(FormaPagamento.id)
                .filter_by(tipo_forma_pagamento=4)
                .first()
            )

            if (campanha := db.session.get(Campanha, fk_campanha_id)) is None:
                response = {"error": "Campanha não encontrada."}
                log_access(
                    response,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response, 404

            if (
                endereco := Endereco.query.filter_by(
                    fk_clifor_id=clifor.id
                ).first()
            ) is None:
                response = {"error", "Endereço não encontrado."}
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

            payload_payment = {
                "additional_info": {
                    "ip_address": request.remote_addr,
                    "items": [
                        {
                            "id": str(uuid.uuid4()),
                            "title": campanha.titulo,
                            "description": f"doação para a campanha {campanha.titulo}",
                            "unit_price": float(valor_doacao),
                            "type": "donation",
                            "warranty": False,
                            "category_descriptor": {
                                "passenger": {},
                                "route": {},
                            },
                        }
                    ],
                    "payer": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone": {
                            "area_code": codigo_area,
                            "number": telefone,
                        },
                        "address": {
                            "zip_code": endereco.cep,
                            "street_name": endereco.rua,
                            "street_number": endereco.numero,
                        },
                    },
                },
                "transaction_amount": valor_doacao,
                "description": f"Doação para a campanha {campanha.titulo}",
                "installments": 1,
                "capture": True,
                "token": card_token.get("id"),
                "statement_descriptor": "MercadoPago.Hesed",
                "payer": {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "identification": {
                        "type": tipo_documento,
                        "number": cpf_cnpj,
                    },
                    "address": {
                        "zip_code": endereco.cep,
                        "street_name": endereco.rua,
                        "street_number": endereco.numero,
                        "neighborhood": endereco.bairro,
                        "city": endereco.cidade,
                        "federal_unit": endereco.estado,
                    },
                },
            }

            response_mp = mp.create_payment(payload_payment, device_id)

            use_case = PaymentCreditCardUseCase()

            response = use_case.format_response(response_mp)
            response_mp["msg"] = response["message"]

            if response["status"] == "rejected":
                log_access(
                    response_mp,
                    current_user["id"],
                    current_user["nome"],
                    current_user["fk_perfil_id"],
                )
                return response_mp, 200

            register_order(
                campanha=campanha,
                clifor=clifor,
                reference_num=reference_num,
                valor_doacao=valor_doacao,
                forma_pagamento=forma_pagamento.id,
                periodo=1,
                id_pedido=response_mp.get("id"),
                id_transacao=response_mp.get("id"),
                fk_gateway_pagamento_id=self.__payment_setup,
                status_processamento=1,
            )

            log_access(
                response_mp,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )

            return response_mp, 201

        except MercadoPagoException as exception:
            error = translator.translate(exception.error_message)
            response = {"error": error}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, exception.status_code

        except KeyError as exception:
            response = {"error": f"O campo {exception} é obrigatório."}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 400

        except ValueError as exception:
            response = {"error": str(exception)}
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 400

        except Exception as exception:
            response = {
                "error": "Ocorreu um erro ao criar o pagamento.",
                "type_error": str(type(exception)),
                "msg_error": str(exception),
            }
            log_access(
                response,
                current_user["id"],
                current_user["nome"],
                current_user["fk_perfil_id"],
            )
            return response, 500
