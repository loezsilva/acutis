from datetime import datetime
from http import HTTPStatus

from flask.testing import FlaskClient


def test_buscar_card_doacoes_sucesso(
    client: FlaskClient, seed_campanha_doacao, seed_dados_doacao
):
    campanha = seed_campanha_doacao
    lead, _ = seed_dados_doacao(campanha=campanha)

    payload = {'email': lead.email, 'senha': '@Teste;1234'}  # NOSONAR

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    response = client.get(
        '/api/membros/buscar-card-doacoes',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'total_pago_doacoes': {'quantidade_doacoes': 1, 'valor_doado': 10.0},
        'ultima_doacao_paga': {
            'ultima_doacao': datetime.today().strftime('%d/%m/%Y')
        },
    }


def test_buscar_card_doacoes_erro_doacao_nao_encontrada(
    client: FlaskClient,
    membro_token,
):
    response = client.get(
        '/api/membros/buscar-card-doacoes',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Nenhuma doação encontrada.'}]
