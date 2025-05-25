from http import HTTPStatus
from unittest.mock import patch

from authlib.integrations.flask_client import OAuth
from faker import Faker
from flask.testing import FlaskClient

from acutis_api.infrastructure.extensions import database
from tests.factories import LeadFactory

faker = Faker('pt-BR')


def test_login_google_redirecionamento_sucesso(client: FlaskClient):
    response = client.get('/api/autenticacao/google/authorize')

    assert response.status_code == HTTPStatus.FOUND
    assert 'https://accounts.google.com/o/oauth2/v2/auth' in response.location


@patch.object(OAuth, 'create_client')
def test_google_callback_sucesso(mock_create_client, client: FlaskClient):
    with client.session_transaction() as sess:
        sess['original_url'] = 'https://labs.institutohesed.org.br/'

    mock_google = mock_create_client.return_value
    mock_google.authorize_access_token.return_value = {
        'access_token': 'mock_access_token',
        'userinfo': {
            'sub': '123456789',
            'name': 'Mock User',
            'email': 'mockuser@example.com',
        },
    }

    response = client.get('/api/autenticacao/google/callback')

    assert response.status_code == HTTPStatus.FOUND


@patch.object(OAuth, 'create_client')
def test_google_callback_login_forbidden(
    mock_create_client, client: FlaskClient
):
    with client.session_transaction() as sess:
        sess['original_url'] = 'https://labs.institutohesed.org.br/'

    lead = LeadFactory()
    lead.senha = '#Teste@1234'
    database.session.add(lead)
    database.session.commit()

    mock_google = mock_create_client.return_value
    mock_google.authorize_access_token.return_value = {
        'access_token': 'mock_access_token',
        'userinfo': {
            'sub': '123456789',
            'name': 'Mock User',
            'email': lead.email,
        },
    }

    response = client.get('/api/autenticacao/google/callback')

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.get_json() == [
        {
            'msg': 'Ative sua conta pelo link enviado ao seu e-mail antes de fazer login.'  # noqa
        }
    ]


@patch.object(OAuth, 'create_client')
def test_google_callback_login_sucesso(
    mock_create_client, client: FlaskClient
):
    with client.session_transaction() as sess:
        sess['original_url'] = 'https://labs.institutohesed.org.br/'

    lead = LeadFactory(status=True)
    lead.senha = '#Teste@1234'
    database.session.add(lead)
    database.session.commit()

    mock_google = mock_create_client.return_value
    mock_google.authorize_access_token.return_value = {
        'access_token': 'mock_access_token',
        'userinfo': {
            'sub': '123456789',
            'name': 'Mock User',
            'email': lead.email,
        },
    }

    response = client.get('/api/autenticacao/google/callback')

    assert response.status_code == HTTPStatus.FOUND
