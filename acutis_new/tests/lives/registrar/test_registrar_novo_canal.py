from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

REGISTRAR_NOVO_CANAL_ENDPOINT = '/api/admin/lives/criar-canal'
JSON_CONTENT_TYPE = 'application/json'

faker = Faker(locale='pt-BR')


def test_criar_canal_sucesso(client, seed_nova_campanha, membro_token):
    campanha = seed_nova_campanha()

    payload = {
        'campanha_id': str(campanha.id),
        'rede_social': 'youtube',
        'tag': faker.word(),
    }

    response = client.post(
        REGISTRAR_NOVO_CANAL_ENDPOINT,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json['msg'] == 'Canal criado com sucesso.'


def test_criar_canal_conflito(client, seed_nova_campanha, membro_token):
    campanha = seed_nova_campanha()

    canal_existente = {
        'campanha_id': str(campanha.id),
        'rede_social': 'youtube',
        'tag': 'canal-existente',
    }

    client.post(
        REGISTRAR_NOVO_CANAL_ENDPOINT,
        json=canal_existente,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    payload = {
        'campanha_id': str(campanha.id),
        'rede_social': 'youtube',
        'tag': 'canal-existente',
    }

    response = client.post(
        REGISTRAR_NOVO_CANAL_ENDPOINT,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json[0]['msg'] == 'Canal já cadastrado.'


def test_criar_canal_dados_invalidos(client: FlaskClient, membro_token):
    payload = {
        'fk_campanha_id': '123e4567-e89b-12d3-a456-426614174000',
        'rede_social': '',
        'tag': '',
    }

    response = client.post(
        REGISTRAR_NOVO_CANAL_ENDPOINT,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_criar_canal_sem_autenticacao(client: FlaskClient):
    payload = {
        'fk_campanha_id': '123e4567-e89b-12d3-a456-426614174000',
        'rede_social': 'youtube',
        'tag': 'canal-existente',
    }

    response = client.post(
        REGISTRAR_NOVO_CANAL_ENDPOINT,
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
