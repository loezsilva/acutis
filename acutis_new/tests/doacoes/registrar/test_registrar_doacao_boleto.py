import random
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.communication.responses.doacoes import (
    RegistrarDoacaoBoletoResponse,
)
from acutis_api.infrastructure.extensions import database
from acutis_api.infrastructure.services.itau import ItauPixService
from tests.factories import BenfeitorFactory, CampanhaFactory, LeadFactory

PAYLOAD_RETORNO_BOLETO = {  # noqa
    'codigo_canal_operacao': 'API',
    'codigo_operador': '382799864',
    'etapa_processo_boleto': 'efetivacao',
    'beneficiario': {
        'id_beneficiario': '382700998646',
        'nome_cobranca': 'INSTITUTO HESED DOS IRMAOS E I',
        'tipo_pessoa': {
            'codigo_tipo_pessoa': 'J',
            'numero_cadastro_nacional_pessoa_juridica': '02779337000174',
        },
        'endereco': {
            'nome_logradouro': 'AV DIONISIO LEONEL ALENCAR, 1443,  ',
            'nome_bairro': 'ANCURI',
            'nome_cidade': 'FORTALEZA',
            'sigla_UF': 'CE',
            'numero_CEP': '60873073',
            'numero': '1443',
            'complemento': ' ',
        },
    },
    'dado_boleto': {
        'descricao_instrumento_cobranca': 'boleto_pix',
        'tipo_boleto': 'a vista',
        'codigo_carteira': '109',
        'valor_total_titulo': '00000000000001000',
        'codigo_especie': '99',
        'data_emissao': '2025-05-26',
        'pagador': {
            'pessoa': {
                'nome_pessoa': 'Leonardo Neville Barbosa Guimarães',
                'tipo_pessoa': {
                    'codigo_tipo_pessoa': 'F',
                    'numero_cadastro_pessoa_fisica': '60618327371',
                },
            },
            'endereco': {
                'nome_logradouro': 'Av. Alberto Craveiro',
                'nome_bairro': 'Boa Vista',
                'nome_cidade': 'Fortaleza',
                'sigla_UF': 'CE',
                'numero_CEP': '60861212',
            },
            'pagador_eletronico_DDA': False,
            'praca_protesto': False,
        },
        'sacador_avalista': {
            'pessoa': {
                'nome_pessoa': 'INSTITUTO HESED DOS IRMAOS E IRMAS',
                'tipo_pessoa': {
                    'codigo_tipo_pessoa': 'J',
                    'numero_cadastro_nacional_pessoa_juridica': '02779337000174',  # noqa
                },
            },
            'endereco': {
                'nome_logradouro': 'AVENIDA DIONISIO LEONEL ALENCAR',
                'nome_bairro': 'ANCURI',
                'nome_cidade': 'FORTALEZA',
                'sigla_UF': 'CE',
                'numero_CEP': '60873073',
            },
        },
        'dados_individuais_boleto': [
            {
                'id_boleto_individual': 'eb42a6c4-be7b-4839-9978-acfff59c85fe',
                'numero_nosso_numero': '22015787',
                'dac_titulo': '8',
                'data_vencimento': '2025-06-26',
                'valor_titulo': '00000000000001000',
                'codigo_barras': '34192112400000010001092201578783827998646000',  # noqa
                'numero_linha_digitavel': (
                    '34191092220157878382979986460008211240000001000'
                ),
                'data_limite_pagamento': '2025-06-26',
                'lista_mensagens_cobranca': [],
            }
        ],
        'codigo_tipo_vencimento': 3,
        'data_limite_pagamento': '2025-06-26',
        'pagamento_parcial': False,
        'quantidade_maximo_parcial': '0',
        'recebimento_divergente': {
            'codigo_tipo_autorizacao': '03',
            'codigo_tipo_recebimento': 'P',
            'percentual_minimo': '00000000000000000',
            'percentual_maximo': '00000000000000000',
        },
        'desconto_expresso': False,
    },
    'dados_qrcode': {
        'chave': 'acaf8e2c-a0e1-460c-a632-fae4f2024b2f',
        'emv': '00020101021226770014BR.GOV.BCB.PIX2555api.itau/pix/qr/v2/ff92babc-646d-4c20-8d32-8d3159e85d105204000053039865802BR5925INSTITUTO HESED DOS IRMAO6009FORTALEZA62070503***63049B78',  # noqa
        'base64': 'iVBORw0KGgoAAAANSUhEUgAAAPoAAAD6AQAAAACgl2eQAAACzElEQVR4Xu2XQXIjIRAE4SPw/1/sU+Aj4MzGYY11cOzB074MIWnHkI7ora4u5LJ/Xv/K+87beoCzHuCsBzjr/4BRSh19ldZXY5W+R59uJgKT14JpDW7I1VHdzAT4cZS64nPuVfdq1c1kYKJUn4qGUGr2J0BDqhpVjtbPZibgC234nB6s8/S9mzcD+nO+r3dXv5//MuDStHSJ8lbXvZ/baQAn+AXHtOLCLzz2S7MSADfqXBamd49lqLQnApTJoVb1rVCdZhEmmcAwPkkQBJtIFO891SkPCIEo1OEFjUDdh8gCNMu0R/NkOtOrYpfhvR84sbEjPolys9Qpugh1P4Aqn7Pivdp063Tn8r+4HYjCeNkorhUfGGHKzAROch2Foj6zrDpNaYA2sVtIxkMML/eLncsDrIup0S+ral4btZAsEVh2pmmQEUFydhydPEBrTCeF9OKE9NDAlyITgPBspDd+NUEsGufmAkhUlxEaPeNzmmg7EeDUDcXyAatUd4LIArDq9iLb7nm1UGb8QiJAmwgtJPJf3prFrll/FuD0ynU0omAq1bE8JwJMCH4pDgvWXTEzjnHPBUgMC4wUE3fzFeYZQOPAkobGCd84Sy/TJgCqg0uqQeLVbpndAUoELHLarGWCRbccH8/TANXxL69ujnHG5WKpTSILOKkRU9tOfCFZvyp5PzDUqDqy2w+CZJsoMdFpgAeqRaFhXyLM56/ByQCKTbK2uN35LOXEeR6wkMlSo7aubBEqL6EyAArzPc77ZOgcL9MmAGbXdHKIcyTi+wXHXGovJe8HXDM2/XoTv7AdppoIWBAXCeVhEz3jn6Tzm6NuByxwGWEObEgVlr0mzP0AwXWCI3qEecgyDLyTgShqerUTqlsj/wEwLW05QfEDXPkyTAYg0+0YSnGiY0gQ/ZIG2KFhhJPl8a0PgvT4Pjg3Az+tBzjrAc56gLN+AfgAjT0OGfxrVVcAAAAASUVORK5CYII=',  # noqa
        'txid': 'BL38270099864109000000022015787',
        'id_location': '534489523479496541',
        'location': 'api.itau/pix/qr/v2/ff92babc-646d-4c20-8d32-8d3159e85d10',
        'tipo_cobranca': 'cob',
    },
    'msg': 'Boleto gerado com sucesso',
}


@patch.object(ItauPixService, 'criar_pagamento_bolecode')
def test_registrar_doacao_boleto_sucesso(
    mock_criar_pagamento_bolecode,
    client: FlaskClient,
    seed_campanha_doacao,
    membro_token,
):
    campanha_doacao = seed_campanha_doacao

    nosso_numero = str(random.randrange(10**7, 10**8))
    transacao_id = 'BL38270099864109000000096246975'

    mock_criar_pagamento_bolecode.return_value = (  # NOSONAR
        PAYLOAD_RETORNO_BOLETO,
        transacao_id,
        nosso_numero,
    )

    payload = {
        'campanha_id': campanha_doacao.id,
        'valor_doacao': 10.00,
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/boleto',  # NOSONAR
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert RegistrarDoacaoBoletoResponse.model_validate(response.json)


@patch.object(ItauPixService, 'criar_pagamento_bolecode')
def test_registrar_doacao_boleto_vinculacao_benfeitor_sucesso(
    mock_criar_pagamento_bolecode,
    client: FlaskClient,
    seed_campanha_doacao,
    seed_registrar_membro,
):
    campanha_doacao = seed_campanha_doacao

    nosso_numero = str(random.randrange(10**7, 10**8))
    transacao_id = 'BL38270099864109000000096246975'

    mock_criar_pagamento_bolecode.return_value = (
        PAYLOAD_RETORNO_BOLETO,
        transacao_id,
        nosso_numero,
    )

    lead, membro, _ = seed_registrar_membro(
        status=True, numero_documento='82907783092'
    )
    benfeitor = BenfeitorFactory(
        nome=lead.nome,
        numero_documento=membro.numero_documento,
    )
    database.session.add(benfeitor)
    database.session.commit()
    payload = {'email': lead.email, 'senha': '#Teste;@123'}  # NOSONAR

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false',  # NOSONAR
        json=payload,
    )
    token = resp_token.json['access_token']

    payload = {
        'campanha_id': campanha_doacao.id,
        'valor_doacao': 10.00,
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/boleto',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert RegistrarDoacaoBoletoResponse.model_validate(response.json)


def test_registrar_doacao_boleto_erro_lead_sem_membro(
    client: FlaskClient,
    seed_campanha_doacao,
):
    campanha_doacao = seed_campanha_doacao
    lead = LeadFactory(status=True)
    lead.senha = '#Teste;@123'
    database.session.add(lead)
    database.session.commit()

    payload = {'email': lead.email, 'senha': '#Teste;@123'}

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    payload = {
        'campanha_id': campanha_doacao.id,
        'valor_doacao': 10.00,
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/boleto',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {'msg': 'Complete seu cadastro para realizar uma doação.'}
    ]


def test_registrar_doacao_boleto_erro_campanha_nao_encontrada(
    client: FlaskClient,
    seed_registrar_membro,
):
    lead, membro, _ = seed_registrar_membro(
        status=True, numero_documento='82907783092'
    )
    benfeitor = BenfeitorFactory(
        nome=lead.nome,
        numero_documento=membro.numero_documento,
    )
    database.session.add(benfeitor)
    database.session.commit()
    payload = {'email': lead.email, 'senha': '#Teste;@123'}

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    payload = {
        'campanha_id': '5850195c-ed57-4d7f-b166-3ab3f0e44c64',
        'valor_doacao': 10.00,
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/boleto',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Campanha não encontrada.'}]


def test_registrar_doacao_boleto_erro_campanha_inativa(
    client: FlaskClient,
    seed_registrar_membro,
):
    lead, membro, _ = seed_registrar_membro(
        status=True, numero_documento='82907783092'
    )
    benfeitor = BenfeitorFactory(
        nome=lead.nome,
        numero_documento=membro.numero_documento,
    )
    database.session.add(benfeitor)
    database.session.commit()
    payload = {'email': lead.email, 'senha': '#Teste;@123'}

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    campanha = CampanhaFactory(ativa=False, criado_por=membro.id)
    database.session.add(campanha)
    database.session.commit()

    payload = {
        'campanha_id': campanha.id,
        'valor_doacao': 10.00,
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/boleto',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {'msg': 'Doações para essa campanha estão indisponíveis no momento.'}
    ]


def test_registrar_doacao_boleto_erro_identidade_estrangeira(
    client: FlaskClient,
    seed_registrar_membro,
    seed_campanha_doacao,
):
    campanha = seed_campanha_doacao

    lead, membro, _ = seed_registrar_membro(
        status=True, numero_documento='62143598'
    )
    benfeitor = BenfeitorFactory(
        nome=lead.nome,
        numero_documento=membro.numero_documento,
    )
    database.session.add(benfeitor)
    database.session.commit()
    payload = {'email': lead.email, 'senha': '#Teste;@123'}

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    payload = {
        'campanha_id': campanha.id,
        'valor_doacao': 10.00,
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/boleto',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {
            'msg': 'Você precisa ter um CPF ou CNPJ cadastrado para doar por este meio de pagamento.'  # noqa
        }
    ]
