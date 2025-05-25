from http import HTTPStatus

from flask.testing import FlaskClient


def test_esqueceu_senha_sucesso(client: FlaskClient, seed_registrar_membro):
    lead = seed_registrar_membro(status=True)[0]

    payload = {'email': lead.email}

    response = client.post('/api/autenticacao/recuperar-senha', json=payload)

    assert response.status_code == HTTPStatus.OK
    assert response.json == {'msg': 'Email enviado com sucesso.'}


def test_esqueceu_senha_email_invalido(client: FlaskClient):
    payload = {'email': 'email@email.com'}

    response = client.post('/api/autenticacao/recuperar-senha', json=payload)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [
        {
            'msg': 'Lamentamos que não foi possível identificá-lo'
            'segundo as informações fornecidas.'
        }
    ]
