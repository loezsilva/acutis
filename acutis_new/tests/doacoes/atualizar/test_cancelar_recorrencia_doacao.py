import uuid
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.infrastructure.services.maxipago import MaxiPago


@patch.object(MaxiPago, 'cancelar_pagamento_recorrente')
def test_cancelar_recorrencia_doacao_sucesso(  # NOSONAR
    mock_cancelar_pagamento_recorrente,
    client: FlaskClient,
    seed_campanha_doacao,
    seed_dados_doacao,
):
    mock_cancelar_pagamento_recorrente.return_value

    campanha = seed_campanha_doacao
    lead, doacao = seed_dados_doacao(campanha=campanha, doacao_ativa=True)

    payload = {'email': lead.email, 'senha': '@Teste;1234'}

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    response = client.post(
        f'/api/doacoes/pagamento/cancelar-recorrencia/{doacao.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Doação recorrente cancelada com sucesso.'}


def test_cancelar_recorrencia_erro_doacao_nao_encontrada(  # NOSONAR
    client: FlaskClient, membro_token
):
    doacao_inexistente_id = str(uuid.uuid4())

    response = client.post(
        f'/api/doacoes/pagamento/cancelar-recorrencia/{doacao_inexistente_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json[0] == {
        'msg': f'Ops, doação recorrente com id {doacao_inexistente_id} não encontrada.'  # noqa
    }


def test_cancelar_recorrencia_erro_doacao_status_cancelado(  # NOSONAR
    client: FlaskClient, seed_campanha_doacao, seed_dados_doacao
):
    campanha = seed_campanha_doacao
    lead, doacao = seed_dados_doacao(campanha=campanha, doacao_ativa=False)

    payload = {'email': lead.email, 'senha': '@Teste;1234'}

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    response = client.post(
        f'/api/doacoes/pagamento/cancelar-recorrencia/{doacao.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json[0] == {
        'msg': 'Esta doação já se encontra com status cancelado.'
    }


def test_cancelar_recorrencia_erro_sem_permissao(  # NOSONAR
    client: FlaskClient, seed_campanha_doacao, seed_dados_doacao, membro_token
):
    campanha = seed_campanha_doacao
    _, doacao = seed_dados_doacao(campanha=campanha, doacao_ativa=True)

    response = client.post(
        f'/api/doacoes/pagamento/cancelar-recorrencia/{doacao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json[0] == {
        'msg': 'Você não tem permissão para cancelar esta doação.'
    }
