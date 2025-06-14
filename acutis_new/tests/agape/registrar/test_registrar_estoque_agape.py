from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

REGISTRAR_ITEM_ESTOQUE_AGAPE_ENDPOINT = '/api/agape/registrar-item'

faker = Faker(locale='pt-BR')


def test_registrar_item_estoque_sucesso(client: FlaskClient, membro_token):
    item = faker.name()

    response = client.post(
        REGISTRAR_ITEM_ESTOQUE_AGAPE_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'item': item},
    )

    assert response.status_code == HTTPStatus.CREATED


def test_erro_registrar_item_estoque_existente(
    client: FlaskClient, membro_token, seed_item_estoque_agape
):
    item = seed_item_estoque_agape.item

    response = client.post(
        REGISTRAR_ITEM_ESTOQUE_AGAPE_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'item': item},
    )
    assert response.status_code == HTTPStatus.CONFLICT


def test_erro_registrar_item_estoque_sem_item(
    client: FlaskClient,
    membro_token,
):
    response = client.post(
        REGISTRAR_ITEM_ESTOQUE_AGAPE_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_erro_registrar_item_estoque_sem_token(
    client: FlaskClient,
):
    response = client.post(
        REGISTRAR_ITEM_ESTOQUE_AGAPE_ENDPOINT,
        json={'item': 'item'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
