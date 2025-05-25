from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.domain.services.schemas.maxipago import PagamentoResponse
from acutis_api.infrastructure.extensions import database
from acutis_api.infrastructure.services.maxipago import MaxiPago
from tests.factories import BenfeitorFactory, CampanhaFactory, LeadFactory


@patch.object(MaxiPago, 'criar_pagamento_unico')
def test_registrar_doacao_cartao_credito_sucesso(  # NOSONAR
    mock_criar_pagamento_unico,
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
):
    campanha_doacao = seed_campanha_doacao

    mock_criar_pagamento_unico.return_value = PagamentoResponse(
        orderID='54042aab-1e3a-4b46-85c6-9209c4a3d01b',
        referenceNum='cef47fc5-6a31-4124-ad55-501df7370778_CARTAO_1744650661.626459',
        transactionID='738366809',
    )

    payload = {
        'campanha_id': campanha_doacao.id,
        'codigo_seguranca': '784',
        'nome_titular': 'Leonardo Guimaraes',
        'numero_cartao': '4578 6985 2354 1456',
        'numero_documento': '76825523015',
        'valor_doacao': 10.00,
        'vencimento_ano': '2028',
        'vencimento_mes': '11',
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/cartao-de-credito',
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Doação realizada com sucesso.'}


@patch.object(MaxiPago, 'criar_pagamento_recorrente')
def test_registrar_doacao_cartao_credito_recorrente_sucesso(  # NOSONAR
    mock_criar_pagamento_recorrente,
    client: FlaskClient,
    membro_token,
    seed_campanha_doacao,
):
    campanha_doacao = seed_campanha_doacao

    mock_criar_pagamento_recorrente.return_value = PagamentoResponse(
        orderID='54042aab-1e3a-4b46-85c6-9209c4a3d01b',
        referenceNum='cef47fc5-6a31-4124-ad55-501df7370778_CARTAO_1744650661.626459',
        transactionID='738366809',
    )

    payload = {
        'campanha_id': campanha_doacao.id,
        'codigo_seguranca': '784',
        'nome_titular': 'Leonardo Guimaraes',
        'numero_cartao': '4578 6985 2354 1456',
        'numero_documento': '76825523015',
        'valor_doacao': 10.00,
        'vencimento_ano': '2028',
        'vencimento_mes': '11',
        'recorrente': True,
    }

    response = client.post(
        '/api/doacoes/pagamento/cartao-de-credito',
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Doação realizada com sucesso.'}


@patch.object(MaxiPago, 'criar_pagamento_unico')
def test_registrar_doacao_cartao_credito_vinculacao_benfeitor_sucesso(  # NOSONAR # noqa
    mock_criar_pagamento_unico,
    client: FlaskClient,
    seed_registrar_membro,
    seed_campanha_doacao,
):
    campanha_doacao = seed_campanha_doacao

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

    mock_criar_pagamento_unico.return_value = PagamentoResponse(
        orderID='54042aab-1e3a-4b46-85c6-9209c4a3d01b',
        referenceNum='cef47fc5-6a31-4124-ad55-501df7370778_CARTAO_1744650661.626459',
        transactionID='738366809',
    )

    payload = {
        'campanha_id': campanha_doacao.id,
        'codigo_seguranca': '784',
        'nome_titular': 'Leonardo Guimaraes',
        'numero_cartao': '4578 6985 2354 1456',
        'numero_documento': '76825523015',
        'valor_doacao': 10.00,
        'vencimento_ano': '2028',
        'vencimento_mes': '11',
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/cartao-de-credito',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {'msg': 'Doação realizada com sucesso.'}


def test_registrar_doacao_cartao_credito_erro_lead_sem_membro(  # NOSONAR
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
        'codigo_seguranca': '784',
        'nome_titular': 'Leonardo Guimaraes',
        'numero_cartao': '4578 6985 2354 1456',
        'numero_documento': '76825523015',
        'valor_doacao': 10.00,
        'vencimento_ano': '2028',
        'vencimento_mes': '11',
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/cartao-de-credito',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {'msg': 'Complete seu cadastro para realizar uma doação.'}
    ]


@patch.object(MaxiPago, 'criar_pagamento_unico')
def test_registrar_doacao_cartao_credito_erro_campanha_nao_encontrada(  # NOSONAR # noqa
    mock_criar_pagamento_unico,
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

    mock_criar_pagamento_unico.return_value = PagamentoResponse(
        orderID='54042aab-1e3a-4b46-85c6-9209c4a3d01b',
        referenceNum='cef47fc5-6a31-4124-ad55-501df7370778_CARTAO_1744650661.626459',
        transactionID='738366809',
    )

    payload = {
        'campanha_id': '5850195c-ed57-4d7f-b166-3ab3f0e44c64',
        'codigo_seguranca': '784',
        'nome_titular': 'Leonardo Guimaraes',
        'numero_cartao': '4578 6985 2354 1456',
        'numero_documento': '76825523015',
        'valor_doacao': 10.00,
        'vencimento_ano': '2028',
        'vencimento_mes': '11',
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/cartao-de-credito',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Campanha não encontrada.'}]


@patch.object(MaxiPago, 'criar_pagamento_unico')
def test_registrar_doacao_cartao_credito_erro_campanha_inativa(  # NOSONAR
    mock_criar_pagamento_unico,
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

    mock_criar_pagamento_unico.return_value = PagamentoResponse(
        orderID='54042aab-1e3a-4b46-85c6-9209c4a3d01b',
        referenceNum='cef47fc5-6a31-4124-ad55-501df7370778_CARTAO_1744650661.626459',
        transactionID='738366809',
    )

    campanha = CampanhaFactory(ativa=False, criado_por=membro.id)
    database.session.add(campanha)
    database.session.commit()

    payload = {
        'campanha_id': campanha.id,
        'codigo_seguranca': '784',
        'nome_titular': 'Leonardo Guimaraes',
        'numero_cartao': '4578 6985 2354 1456',
        'numero_documento': '76825523015',
        'valor_doacao': 10.00,
        'vencimento_ano': '2028',
        'vencimento_mes': '11',
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/cartao-de-credito',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == [
        {'msg': 'Doações para essa campanha estão indisponíveis no momento.'}
    ]


def test_registrar_doacao_cartao_credito_erro_valor_abaixo_de_10(
    client: FlaskClient,
    membro_token,
):
    payload = {
        'campanha_id': 'a4b1f539-120a-4106-8ccf-a52f2e60fadd',
        'codigo_seguranca': '784',
        'nome_titular': 'Leonardo Guimaraes',
        'numero_cartao': '4578 6985 2354 1456',
        'numero_documento': '76825523015',
        'valor_doacao': 9.99,
        'vencimento_ano': '2028',
        'vencimento_mes': '11',
        'recorrente': False,
    }

    response = client.post(
        '/api/doacoes/pagamento/cartao-de-credito',
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json[0]['msg'] == (
        'O valor deve ser maior ou igual a R$ 10,00.'
    )
