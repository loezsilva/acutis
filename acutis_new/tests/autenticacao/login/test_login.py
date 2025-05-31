from http import HTTPStatus

from flask.testing import FlaskClient

ROTA_LOGIN = '/api/autenticacao/login'
SENHA_TESTE = '#Teste;@123'


def test_login_sucesso(client: FlaskClient, seed_registrar_membro):
    lead = seed_registrar_membro(status=True)[0]
    payload = {'email': lead.email, 'senha': SENHA_TESTE}

    response = client.post(f'{ROTA_LOGIN}?httponly=false', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json


def test_login_erro_email_incorreto(client: FlaskClient):
    payload = {'email': 'emailinexistente@gmail.com', 'senha': SENHA_TESTE}

    response = client.post(ROTA_LOGIN, json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Ops, email ou senha incorretos.'}]


def test_login_erro_senha_incorreta(
    client: FlaskClient, seed_registrar_membro
):
    lead = seed_registrar_membro(status=True)[0]
    payload = {'email': lead.email, 'senha': 'algumasenha'}

    response = client.post(ROTA_LOGIN, json=payload)

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Ops, email ou senha incorretos.'}]


def test_login_erro_conta_inativa(client: FlaskClient, seed_registrar_membro):
    lead = seed_registrar_membro()[0]
    payload = {'email': lead.email, 'senha': SENHA_TESTE}

    response = client.post(ROTA_LOGIN, json=payload)

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == [
        {
            'msg': 'Ative sua conta pelo link enviado ao seu e-mail antes de fazer login.'  # noqa
        }
    ]
