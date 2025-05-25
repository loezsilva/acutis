from datetime import timedelta
import logging
import random
from typing import Any
from uuid import uuid4

from flask import jsonify
from builder import db
from models.campanha import Campanha
from models.clifor import Clifor
from models.endereco import Endereco
from models.pedido import Pedido
from models.processamento_pedido import ProcessamentoPedido
from services.itau_api import ItauAPI
from utils.functions import get_current_time


class GetPixInvoicePaymentCode:
    def __init__(self) -> None:
        pass

    def execute(self, fk_processamento_pedido_id: int):
        processamento_pedido = db.session.get(
            ProcessamentoPedido, fk_processamento_pedido_id
        )

        error_response = self.__validate_payment_status(processamento_pedido)
        if error_response:
            return error_response

        pedido = db.session.get(Pedido, processamento_pedido.fk_pedido_id)

        if pedido.fk_gateway_pagamento_id != 1:
            return {
                "error": "Código de pagamento para este gateway ainda não está disponível."
            }, 400

        if processamento_pedido.transaction_id:
            return self.__get_payment_code(processamento_pedido)
        else:
            return self.__create_payment_code(processamento_pedido)

    def __validate_payment_status(self, processamento_pedido):
        if processamento_pedido.status_processamento == 1:
            return {"error": "O status do pedido se encontra como pago."}, 409
        return None

    def __get_payment_code(self, processamento_pedido):
        match processamento_pedido.fk_forma_pagamento_id:
            case 2:
                return self.__get_itau_pix_payment(
                    processamento_pedido.transaction_id
                )
            case 3:
                return self.__get_itau_invoice_payment(
                    processamento_pedido.nosso_numero
                )
            case _:
                return {
                    "error": "O código para esta forma de pagamento não está disponível."
                }, 400

    def __create_payment_code(self, processamento_pedido):
        match processamento_pedido.fk_forma_pagamento_id:
            case 2:
                return self.__create_itau_pix_payment(processamento_pedido)
            case 3:
                return self.__create_itau_invoice_payment(processamento_pedido)
            case _:
                return {
                    "error": "O código para esta forma de pagamento não está disponível."
                }, 400

    def __get_itau_pix_payment(self, transaction_id: str):
        itau_api = ItauAPI("pix")

        get_pix_payment, status_code_pix = itau_api.get(
            path=f"/cobv/{transaction_id}"
        )

        if status_code_pix not in [200, 201, 204]:
            return {"error": "Ocorreu um erro ao buscar o pagamento."}, 500

        if get_pix_payment["status"] != "ATIVA":
            return {"error": "Este pagamento não está mais ativo."}, 400

        get_qrcode_payment, status_code_qrcode = itau_api.get(
            path=f"/cobv/{transaction_id}/qrcode"
        )

        if status_code_qrcode not in [200, 201, 204]:
            return {
                "error": "Ocorreu um erro ao gerar o qrcode de pagamento."
            }, 500

        response = {"codigo_pagamento": get_qrcode_payment.get("emv")}

        return response, 200

    def __create_itau_pix_payment(self, processamento_pedido: Any):
        clifor = db.session.get(Clifor, processamento_pedido.fk_clifor_id)
        if not clifor:
            return {"error": "cliente não encontrado."}, 404

        pedido = db.session.get(Pedido, processamento_pedido.fk_pedido_id)

        campanha = db.session.get(Campanha, pedido.fk_campanha_id)
        if not campanha:
            return {"error": "Campanha para doação não encontrada."}, 404

        if not campanha.status:
            return {"error": "Esta campanha foi encerrada."}, 403

        DEVEDOR_MAP = {
            11: {"cpf": clifor.cpf_cnpj, "nome": clifor.nome},
            14: {"cnpj": clifor.cpf_cnpj, "nome": clifor.nome},
        }

        data_vencimento_obj = get_current_time() + timedelta(days=31)
        data_vencimento = data_vencimento_obj.strftime("%Y-%m-%d")

        TxID = uuid4().hex
        path_put = f"/cobv/{TxID}"
        path_get = path_put + "/qrcode"
        devedor = DEVEDOR_MAP[len(clifor.cpf_cnpj)]

        body = {
            "calendario": {
                "dataDeVencimento": data_vencimento,
                "validadeAposVencimento": 0,
            },
            "devedor": devedor,
            "valor": {"original": float(processamento_pedido.valor)},
            "chave": campanha.chave_pix,
        }

        itau_api = ItauAPI("pix")

        response_put, status_put = itau_api.put(path=path_put, body=body)
        response_get, status_get = itau_api.get(path=path_get)

        if status_put != 201:
            return {
                "error": "Ocorreu um erro ao gerar o pagamento.",
                "type_error": str(status_put),
                "msg_error": str(response_put),
            }, 500

        if status_get != 200:
            return {
                "error": "Ocorreu um erro ao retornar os dados de pagamento",
                "type_error": str(status_get),
                "msg_error": str(response_get),
            }, 500

        processamento_pedido.data_processamento = get_current_time()
        processamento_pedido.transaction_id = TxID

        db.session.commit()

        response = {"codigo_pagamento": response_get.get("emv")}

        return response, 200

    def __get_itau_invoice_payment(self, nosso_numero: str):
        itau_api = ItauAPI("boleto")

        data, status_code = itau_api.get(
            path=f"/boletos?id_beneficiario=382700998646&nosso_numero={nosso_numero}"
        )

        if status_code not in [200, 201, 204]:
            return {"error": "Ocorreu um erro ao buscar o pagamento."}, 500

        if len(data["data"]) < 1:
            return {
                "error": "O boleto ainda está sendo gerado. Tente novamente mais tarde!"
            }, 500

        response = data["data"][0]
        print(response)
        response["msg"] = "Boleto gerado com sucesso."

        return response, 200

    def __create_itau_invoice_payment(self, processamento_pedido: Any):
        clifor = db.session.get(Clifor, processamento_pedido.fk_clifor_id)
        if not clifor:
            return {"error": "cliente não encontrado."}, 404

        pedido = db.session.get(Pedido, processamento_pedido.fk_pedido_id)

        campanha = db.session.get(Campanha, pedido.fk_campanha_id)
        if not campanha:
            return {"error": "Campanha para doação não encontrada."}, 404

        if not campanha.status:
            return {"error": "Esta campanha foi encerrada."}, 403

        endereco = Endereco.query.filter_by(fk_clifor_id=clifor.id).first()
        if not endereco:
            return {"error", "Endereço do usuário não encontrado."}, 404

        valor_boleto = str(int(processamento_pedido.valor * 100)).zfill(17)

        data_vencimento_obj = get_current_time() + timedelta(days=31)
        data_limite_vencimento_obj = data_vencimento_obj

        data_vencimento_boleto = data_vencimento_obj.strftime("%Y-%m-%d")
        data_limite_vencimento = data_limite_vencimento_obj.strftime(
            "%Y-%m-%d"
        )

        numero_nosso_numero = random.randrange(10**7, 10**8)

        path = "/boletos_pix"

        TIPO_PESSOA_MAP = {
            11: {
                "codigo_tipo_pessoa": "F",
                "numero_cadastro_pessoa_fisica": clifor.cpf_cnpj,
            },
            14: {
                "codigo_tipo_pessoa": "J",
                "numero_cadastro_nacional_pessoa_juridica": clifor.cpf_cnpj,
            },
        }

        tipo_pessoa = TIPO_PESSOA_MAP[len(clifor.cpf_cnpj)]

        body = {
            "etapa_processo_boleto": "efetivacao",
            "beneficiario": {"id_beneficiario": "382700998646"},
            "dado_boleto": {
                "tipo_boleto": "a vista",
                "codigo_carteira": "109",
                "valor_total_titulo": valor_boleto,
                "codigo_especie": "99",
                "data_emissao": get_current_time().strftime("%Y-%m-%d"),
                "pagador": {
                    "pessoa": {
                        "nome_pessoa": clifor.nome,
                        "tipo_pessoa": tipo_pessoa,
                    },
                    "endereco": {
                        "nome_logradouro": (
                            endereco.rua
                            if len(endereco.rua) <= 45
                            else endereco.rua[:45]
                        ),
                        "nome_bairro": (
                            endereco.bairro
                            if len(endereco.bairro) <= 15
                            else endereco.bairro[:15]
                        ),
                        "nome_cidade": (
                            endereco.cidade
                            if len(endereco.cidade) <= 20
                            else endereco.cidade[:20]
                        ),
                        "sigla_UF": (
                            endereco.estado
                            if len(endereco.estado) <= 2
                            else endereco.estado[:2]
                        ),
                        "numero_CEP": endereco.cep,
                    },
                },
                "sacador_avalista": {
                    "pessoa": {
                        "nome_pessoa": "INSTITUTO HESED DOS IRMAOS E IRMAS",
                        "tipo_pessoa": {
                            "codigo_tipo_pessoa": "J",
                            "numero_cadastro_nacional_pessoa_juridica": "02779337000174",
                        },
                    },
                    "endereco": {
                        "nome_logradouro": "AVENIDA DIONISIO LEONEL ALENCAR",
                        "nome_bairro": "ANCURI",
                        "nome_cidade": "FORTALEZA",
                        "sigla_UF": "CE",
                        "numero_CEP": "60873073",
                    },
                },
                "dados_individuais_boleto": [
                    {
                        "numero_nosso_numero": numero_nosso_numero,
                        "data_vencimento": data_vencimento_boleto,
                        "valor_titulo": valor_boleto,
                        "data_limite_pagamento": data_limite_vencimento,
                    }
                ],
            },
            "dados_qrcode": {"chave": campanha.chave_pix},
        }

        itau_api = ItauAPI("bolecode")

        resp, status = itau_api.post(path=path, body=body)

        if status != 200:
            logging.error(
                f"type_error: {str(status)} - msg_error: {str(resp)}"
            )
            return {
                "error": "Ocorreu um erro ao criar o boleto de pagamento."
            }, 500

        data = resp["data"]
        numero_linha_digitavel = data["dado_boleto"][
            "dados_individuais_boleto"
        ][0]["numero_linha_digitavel"]

        TxID = data["dados_qrcode"]["txid"]
        nosso_numero = data["dado_boleto"]["dados_individuais_boleto"][0][
            "numero_nosso_numero"
        ]

        processamento_pedido.data_processamento = get_current_time()
        processamento_pedido.transaction_id = TxID
        processamento_pedido.nosso_numero = nosso_numero

        db.session.commit()

        response = {"codigo_pagamento": numero_linha_digitavel}

        return jsonify(response), 201
