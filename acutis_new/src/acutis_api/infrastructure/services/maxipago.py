import logging
from datetime import datetime

import xmltodict
from httpx import Client

from acutis_api.domain.services.schemas.maxipago import (
    DadosPagamento,
    PagamentoResponse,
)
from acutis_api.infrastructure.settings import settings
from acutis_api.shared.errors.maxipago import (
    ERROS_MAXIPAGO,
    ErroPagamento,
    ErroRecorrenciaNaoEncontrada,
)


class MaxiPago:
    def __init__(self):
        self._merchant_id = settings.MAXIPAGO_MERCHANT_ID
        self._merchant_key = settings.MAXIPAGO_MERCHANT_KEY

    def _verificacao_xml(self):
        return f"""
        <verification>
            <merchantId>{self._merchant_id}</merchantId>
            <merchantKey>{self._merchant_key}</merchantKey>
        </verification>
        """

    @staticmethod
    def _enviar_requisicao(xml, url: str):
        headers = {'Content-Type': 'text/xml'}

        with Client() as client:
            response = client.post(url, data=xml, headers=headers)
            response.raise_for_status()

        resp = dict(xmltodict.parse(response.text))
        return resp

    @staticmethod
    def _validar_resposta_xml(resposta: dict):
        status = resposta['transaction-response']['responseCode']
        if status != '0':
            mensagem_maxi = resposta['transaction-response'].get(
                'errorMessage', 'Erro desconhecido.'
            )
            mensagem_dict = ERROS_MAXIPAGO.get(
                status, 'Erro desconhecido na transação.'
            )
            logging.error(f'{mensagem_dict} (Detalhes: {mensagem_maxi})')
            raise ErroPagamento(mensagem_dict)

    @staticmethod
    def _validar_resposta_api(resposta: dict):
        status = resposta['api-response']['errorCode']
        mensagem_erro = resposta['api-response']['errorMessage']
        if status != '0' and 'Invalid' in mensagem_erro:
            raise ErroRecorrenciaNaoEncontrada(
                'A recorrência de pagamento não foi encontrada.'
            )

    def criar_pagamento_unico(
        self, dados_pagamento: DadosPagamento
    ) -> PagamentoResponse:
        xml = f"""
        <transaction-request>
            <version>3.1.1.15</version>
            {self._verificacao_xml()}
            <order>
                <sale>
                    <processorID>5</processorID>
                    <referenceNum>{dados_pagamento.codigo_referencia}</referenceNum>
                    <customerIdExt>{dados_pagamento.numero_documento}</customerIdExt>
                    <billing>
                        <name>{dados_pagamento.nome}</name>
                        <address>{dados_pagamento.rua}</address>
                        <district>{dados_pagamento.bairro}</district>
                        <city>{dados_pagamento.cidade}</city>
                        <state>{dados_pagamento.estado}</state>
                        <postalcode>{dados_pagamento.cep}</postalcode>
                        <country>BR</country>
                        <phone>{dados_pagamento.telefone}</phone>
                        <email>{dados_pagamento.email}</email>
                        <companyName>HeSed</companyName>
                    </billing>
                    <shipping>
                        <name>{dados_pagamento.nome}</name>
                        <address>{dados_pagamento.rua}</address>
                        <district>{dados_pagamento.bairro}</district>
                        <city>{dados_pagamento.cidade}</city>
                        <state>{dados_pagamento.estado}</state>
                        <postalcode>{dados_pagamento.cep}</postalcode>
                        <country>BR</country>
                        <phone>{dados_pagamento.telefone}</phone>
                        <email>{dados_pagamento.email}</email>
                    </shipping>
                    <transactionDetail>
                        <payType>
                            <creditCard>
                                <number>{dados_pagamento.numero_cartao}</number>
                                <expMonth>{dados_pagamento.vencimento_mes}</expMonth>
                                <expYear>{dados_pagamento.vencimento_ano}</expYear>
                                <cvvNumber>{dados_pagamento.codigo_seguranca}</cvvNumber>
                            </creditCard>
                        </payType>
                    </transactionDetail>
                    <payment>
                        <chargeTotal>{dados_pagamento.valor_doacao}</chargeTotal>
                        <currencyCode>BRL</currencyCode>
                    </payment>
                </sale>
            </order>
        </transaction-request>
        """
        response = self._enviar_requisicao(xml, settings.MAXIPAGO_URL_XML)
        self._validar_resposta_xml(response)
        return PagamentoResponse(**response['transaction-response'])

    def criar_pagamento_recorrente(
        self, dados_pagamento: DadosPagamento
    ) -> PagamentoResponse:
        xml = f"""
        <transaction-request>
            <version>3.1.1.15</version>
            {self._verificacao_xml()}
            <order>
                <recurringPayment>
                    <processorID>5</processorID>
                    <referenceNum>{dados_pagamento.codigo_referencia}</referenceNum>
                    <customerIdExt>{dados_pagamento.numero_documento}</customerIdExt>
                    <billing>
                        <name>{dados_pagamento.nome}</name>
                        <address>{dados_pagamento.rua}</address>
                        <district>{dados_pagamento.bairro}</district>
                        <city>{dados_pagamento.cidade}</city>
                        <state>{dados_pagamento.estado}</state>
                        <postalcode>{dados_pagamento.cep}</postalcode>
                        <country>BR</country>
                        <phone>{dados_pagamento.telefone}</phone>
                        <email>{dados_pagamento.email}</email>
                        <companyName>HeSed</companyName>
                    </billing>
                    <shipping>
                        <name>{dados_pagamento.nome}</name>
                        <address>{dados_pagamento.rua}</address>
                        <district>{dados_pagamento.bairro}</district>
                        <city>{dados_pagamento.cidade}</city>
                        <state>{dados_pagamento.estado}</state>
                        <postalcode>{dados_pagamento.cep}</postalcode>
                        <country>BR</country>
                        <phone>{dados_pagamento.telefone}</phone>
                        <email>{dados_pagamento.email}</email>
                    </shipping>
                    <transactionDetail>
                        <payType>
                            <creditCard>
                                <number>{dados_pagamento.numero_cartao}</number>
                                <expMonth>{dados_pagamento.vencimento_mes}</expMonth>
                                <expYear>{dados_pagamento.vencimento_ano}</expYear>
                                <cvvNumber>{dados_pagamento.codigo_seguranca}</cvvNumber>
                            </creditCard>
                        </payType>
                    </transactionDetail>
                    <payment>
                        <chargeTotal>{dados_pagamento.valor_doacao}</chargeTotal>
                        <currencyCode>BRL</currencyCode>
                    </payment>
                    <recurring>
                        <action>new</action>
                        <startDate>{datetime.today().date()}</startDate>
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
        response = self._enviar_requisicao(xml, settings.MAXIPAGO_URL_XML)
        self._validar_resposta_xml(response)
        return PagamentoResponse(**response['transaction-response'])

    def cancelar_pagamento_recorrente(self, codigo_ordem_pagamento: str):
        xml = f"""
        <api-request>
            {self._verificacao_xml()}
            <command>cancel-recurring</command>
            <request>
                <orderID>{codigo_ordem_pagamento}</orderID>
            </request>
        </api-request>
        """
        response = self._enviar_requisicao(xml, settings.MAXIPAGO_URL_API)
        self._validar_resposta_api(response)

    def estornar_pagamento(
        self, codigo_ordem_pagamento: str, codigo_referencia: str, valor: float
    ):
        xml = f"""
        <transaction-request>
            <version>3.1.1.15</version>
            {self._verificacao_xml()}
            <order>
                <return>
                    <orderID>{codigo_ordem_pagamento}</orderID>
                    <referenceNum>{codigo_referencia}</referenceNum>
                    <payment>
                        <chargeTotal>{valor}</chargeTotal>
                    </payment>
                </return>
            </order>
        </transaction-request>
        """
        response = self._enviar_requisicao(xml, settings.MAXIPAGO_URL_XML)
        self._validar_resposta_xml(response)
