from http import HTTPStatus

from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from acutis_api.infrastructure.extensions import database


def test_alterar_senha_sucesso(client: FlaskClient, seed_registrar_membro):
    lead = seed_registrar_membro(status=True)[0]

    access_token = create_access_token(identity=lead.id)

    payload = {
        'senha_atual': '#Teste;@123',
        'nova_senha': '@NovaSenha456',
    }

    response = client.post(
        '/api/autenticacao/alterar-senha',
        json=payload,
        headers={'Authorization': f'Bearer {access_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    assert data == {'msg': 'Senha alterada com sucesso.'}

    database.session.refresh(lead)
    assert lead.verificar_senha('@NovaSenha456') is True


def test_alterar_senha_incorreta(client: FlaskClient, membro_token):
    payload = {
        'senha_atual': '#Teste123456',
        'nova_senha': '@NovaSenha456',
    }

    response = client.post(
        '/api/autenticacao/alterar-senha',
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json == [{'msg': 'A senha atual está incorreta.'}]


def test_senha_curta(client: FlaskClient, membro_token):
    payload = {
        'senha_atual': '#Teste;@123',
        'nova_senha': '123',
    }

    response = client.post(
        '/api/autenticacao/alterar-senha',
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json[0]['msg'] == (
        'A senha deve conter entre 8 a 16 caracteres.'
    )
