import logging
import random
import uuid
from datetime import datetime
from http import HTTPStatus

from httpx import Client

from acutis_api.domain.services.gateway_pagamento import (
    GatewayPagamentoInterface,
)
from acutis_api.domain.services.schemas.gateway_pagamento import (
    BuscarPagamentoPixResponse,
    CriarPagamentoBolecodeRequest,
    CriarPagamentoPixRequest,
)
from acutis_api.exception.errors.bad_request import HttpBadRequestError
from acutis_api.infrastructure.settings import settings


class ItauPixService(GatewayPagamentoInterface):
    def __init__(self):
        self._certificate = './archives/certificado_pix.crt'
        self._key = './archives/chave_pix.key'
        self._cert = (self._certificate, self._key)

    def _buscar_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': settings.ITAU_PIX_CLIENT_ID,
            'client_secret': settings.ITAU_PIX_CLIENT_SECRET,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        with Client(cert=self._cert) as client:
            response = client.post(
                url=settings.ITAU_AUTH_URL, data=payload, headers=headers
            )

        if not HTTPStatus(response.status_code).is_success:
            logging.error(f'Ocorreu um erro ao gerar o token: {response.text}')
            raise Exception('Ocorreu um erro ao gerar o token.')  # NOSONAR

        access_token = response.json()['access_token']
        return access_token

    def criar_pagamento_pix(
        self, pagamento: CriarPagamentoPixRequest
    ) -> BuscarPagamentoPixResponse:
        token = self._buscar_token()
        transacao_id = uuid.uuid4().hex
        url = f'{settings.ITAU_PIX_URL}/cobv/{transacao_id}'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',  # NOSONAR
        }

        payload = {
            'calendario': {
                'dataDeVencimento': pagamento.data_vencimento,
            },
            'devedor': {
                pagamento.tipo_documento: pagamento.numero_documento,
                'nome': pagamento.nome,
            },
            'valor': {'original': pagamento.valor_doacao},
            'chave': pagamento.chave_pix,
        }

        with Client(cert=self._cert) as client:
            response = client.put(url=url, json=payload, headers=headers)

        if not HTTPStatus(response.status_code).is_success:
            logging.error(
                f'Ocorreu um erro ao criar o pagamento PIX: {response.text}'
            )
            raise Exception(  # NOSONAR
                'Ocorreu um erro ao criar o pagamento PIX.'
            )

        return self.buscar_pagamento_pix(transacao_id)

    def buscar_pagamento_pix(
        self, transacao_id: str
    ) -> BuscarPagamentoPixResponse:
        token = self._buscar_token()
        url = f'{settings.ITAU_PIX_URL}/cobv/{transacao_id}/qrcode'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

        with Client(cert=self._cert) as client:
            response = client.get(url=url, headers=headers)

        if not HTTPStatus(response.status_code).is_success:
            logging.error(
                f'Ocorreu um erro ao buscar o pagamento PIX: {response.text}'
            )
            raise Exception(  # NOSONAR
                'Ocorreu um erro ao criar o pagamento PIX.'
            )

        response = response.json()
        return BuscarPagamentoPixResponse(
            pix_copia_cola=response['emv'],
            qrcode=response['imagem_base64'],
            transacao_id=transacao_id,
        )

    def criar_pagamento_bolecode(
        self, dados_pagamento: CriarPagamentoBolecodeRequest
    ):
        token = self._buscar_token()
        url = f'{settings.ITAU_BOLECODE_URL}/boletos_pix'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }
        nosso_numero = random.randrange(10**7, 10**8)
        tipo_pessoa_map = {
            11: {
                'codigo_tipo_pessoa': 'F',
                'numero_cadastro_pessoa_fisica': dados_pagamento.numero_documento,  # noqa
            },
            14: {
                'codigo_tipo_pessoa': 'J',
                'numero_cadastro_nacional_pessoa_juridica': dados_pagamento.numero_documento,  # noqa
            },
        }

        payload = {
            'etapa_processo_boleto': 'efetivacao',
            'beneficiario': {'id_beneficiario': '382700998646'},
            'dado_boleto': {
                'tipo_boleto': 'a vista',
                'codigo_carteira': '109',
                'valor_total_titulo': dados_pagamento.valor_doacao,
                'codigo_especie': '99',
                'data_emissao': datetime.today().strftime('%Y-%m-%d'),
                'pagador': {
                    'pessoa': {
                        'nome_pessoa': dados_pagamento.nome,
                        'tipo_pessoa': tipo_pessoa_map[
                            len(dados_pagamento.numero_documento)
                        ],
                    },
                    'endereco': {
                        'nome_logradouro': (
                            dados_pagamento.rua
                            if len(dados_pagamento.rua) <= 45
                            else dados_pagamento.rua[:45]
                        ),
                        'nome_bairro': (
                            dados_pagamento.bairro
                            if len(dados_pagamento.bairro) <= 15
                            else dados_pagamento.bairro[:15]
                        ),
                        'nome_cidade': (
                            dados_pagamento.cidade
                            if len(dados_pagamento.cidade) <= 20
                            else dados_pagamento.cidade[:20]
                        ),
                        'sigla_UF': (
                            dados_pagamento.estado
                            if len(dados_pagamento.estado) <= 2
                            else dados_pagamento.estado[:2]
                        ),
                        'numero_CEP': dados_pagamento.cep,
                    },
                },
                'sacador_avalista': {
                    'pessoa': {
                        'nome_pessoa': 'INSTITUTO HESED DOS IRMAOS E IRMAS',  # noqa
                        'tipo_pessoa': {
                            'codigo_tipo_pessoa': 'J',
                            'numero_cadastro_nacional_pessoa_juridica': '02779337000174',  # noqa
                        },
                    },
                    'endereco': {
                        'nome_logradouro': 'AVENIDA DIONISIO LEONEL ALENCAR',  # noqa
                        'nome_bairro': 'ANCURI',
                        'nome_cidade': 'FORTALEZA',
                        'sigla_UF': 'CE',
                        'numero_CEP': '60873073',
                    },
                },
                'dados_individuais_boleto': [
                    {
                        'numero_nosso_numero': nosso_numero,
                        'data_vencimento': dados_pagamento.data_vencimento,
                        'valor_titulo': dados_pagamento.valor_doacao,
                        'data_limite_pagamento': dados_pagamento.data_vencimento,  # noqa
                    }
                ],
            },
            'dados_qrcode': {'chave': dados_pagamento.chave_pix},
        }

        with Client(cert=self._cert) as client:
            response = client.post(url=url, json=payload, headers=headers)

        if not HTTPStatus(response.status_code).is_success:
            logging.error(
                f'Ocorreu um erro ao buscar o pagamento Bolecode: {response.text}'  # noqa
            )
            raise Exception(  # NOSONAR
                'Ocorreu um erro ao criar o pagamento Bolecode.'
            )

        response = response.json()
        response = response['data']
        response['msg'] = 'Boleto gerado com sucesso'

        transacao_id = response['dados_qrcode']['txid']

        return response, transacao_id, str(nosso_numero)

    def registra_chave_pix_no_webhook(self, chave_pix):
        path = f'/webhook/{chave_pix}'

        with Client(cert=self._cert) as client:
            _, status_code = client.get(path)
        if status_code != HTTPStatus.OK:
            base_url_api = 'https://api-acutis.institutohesed.org.br'
            body = {'webhookUrl': f'{base_url_api}/webhook/itau'}
            response, status = client.put(path, body)
            if not HTTPStatus(status).is_success:
                logging.error(
                    f'ERRO AO CADASTRAR A CHAVE PIX NO WEBHOOK: {response}'
                )
                razao = 'A chave pix é inválida.'
                raise HttpBadRequestError(
                    razao,
                    response.get('status', 400),
                )
