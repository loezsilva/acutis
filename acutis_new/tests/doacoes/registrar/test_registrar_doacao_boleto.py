import random
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.infrastructure.extensions import database
from acutis_api.infrastructure.services.itau import ItauPixService
from tests.factories import BenfeitorFactory, CampanhaFactory, LeadFactory


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

    mock_criar_pagamento_bolecode.return_value = (
        {'data': {'msg': 'Boleto gerado com sucesso'}},  # NOSONAR
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
    assert response.json == {'data': {'msg': 'Boleto gerado com sucesso'}}


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
        {'data': {'msg': 'Boleto gerado com sucesso'}},
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
        '/api/autenticacao/login?httponly=false',
        json=payload,  # NOSONAR
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
    assert response.json == {'data': {'msg': 'Boleto gerado com sucesso'}}


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
