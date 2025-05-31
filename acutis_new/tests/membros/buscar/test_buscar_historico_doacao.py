import uuid
from datetime import datetime
from http import HTTPStatus

from flask.testing import FlaskClient


def test_buscar_historico_doacao_sucesso(
    client: FlaskClient, seed_campanha_doacao, seed_dados_doacao
):
    quantidade_registros = 1

    campanha = seed_campanha_doacao
    lead, doacao = seed_dados_doacao(campanha=campanha)

    payload = {'email': lead.email, 'senha': '@Teste;1234'}  # NOSONAR

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    response = client.get(
        f'/api/membros/buscar-historico-doacao/{doacao.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == quantidade_registros
    assert response.json['historico_doacao'][0] == {
        'forma_pagamento': 'credito',
        'status_processamento': 'pago',
        'valor_doacao': 10.0,
        'data_doacao': datetime.now().strftime('%d/%m/%Y'),
    }


def test_buscar_historico_doacao_erro_doacao_nao_encontrada(
    client: FlaskClient,
    membro_token,
):
    response = client.get(
        f'/api/membros/buscar-historico-doacao/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Doação não encontrada.'}]


def test_buscar_historico_doacao_erro_permissao_negada(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    campanha = seed_campanha_doacao
    _, doacao = seed_dados_doacao(campanha=campanha)

    response = client.get(
        f'/api/membros/buscar-historico-doacao/{doacao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == [
        {'msg': 'Você não tem permissão para visualizar essa doação.'}
    ]
