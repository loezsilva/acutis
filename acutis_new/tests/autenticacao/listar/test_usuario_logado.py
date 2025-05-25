from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.communication.responses.autenticacao import (
    UsuarioLogadoResponse,
)
from acutis_api.infrastructure.extensions import database
from tests.factories import LeadFactory


def test_usuario_logado(client: FlaskClient, seed_registrar_membro):
    lead, _, _ = seed_registrar_membro(
        nome='Cleiton ativador de conta', status=True
    )

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    response = client.get(
        '/api/autenticacao/usuario-logado',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert UsuarioLogadoResponse.model_validate(response.json)


def test_usuario_logado_nao_membro(client: FlaskClient):
    lead = LeadFactory(
        nome='Cleiton ativador de conta',
        status=True,
    )
    lead.senha = '#Teste;@123'
    database.session.add(lead)
    database.session.commit()

    token = client.post(
        '/api/autenticacao/login?httponly=false',
        json={
            'email': lead.email,
            'senha': '#Teste;@123',
        },
    ).get_json()['access_token']

    response = client.get(
        '/api/autenticacao/usuario-logado',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert UsuarioLogadoResponse.model_validate(response.json)
