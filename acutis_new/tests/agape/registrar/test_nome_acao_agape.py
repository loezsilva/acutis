from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

REGISTRAR_NOME_ACAO_AGAPE_ENDPOINT = '/api/agape/registrar-nome-acao'

faker = Faker(locale='pt-BR')


def test_registrar_nome_acao_sucesso(client: FlaskClient, membro_token):
    nome_acao = faker.name()

    response = client.post(
        REGISTRAR_NOME_ACAO_AGAPE_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={'nome': nome_acao},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert 'id' in response.json
    assert response.json['nome'] == nome_acao


def test_erro_nome_registrar_nome_acao(
    client: FlaskClient, membro_token, seed_nome_acao_agape
):
    nome_acao = seed_nome_acao_agape.nome

    response = client.post(
        REGISTRAR_NOME_ACAO_AGAPE_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
        data={'nome': nome_acao},
    )
    assert response.status_code == HTTPStatus.CONFLICT
