from http import HTTPStatus

from flask.testing import FlaskClient


def test_refresh_token_sucesso(client: FlaskClient, seed_registrar_membro):
    lead = seed_registrar_membro(status=True)[0]
    response = client.post(
        '/api/autenticacao/login?httponly=false',
        json={'email': lead.email, 'senha': '#Teste;@123'},
    )
    refresh_token = response.json['refresh_token']

    response = client.post(
        '/api/autenticacao/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json
