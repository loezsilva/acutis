import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

ROTA = '/api/admin/campanhas/buscar-campanha-por-id'


def test_buscar_campanha_doacao_por_id(
    client: FlaskClient, seed_campanha_doacao, membro_token
):
    response = client.get(
        f'{ROTA}/{seed_campanha_doacao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_buscar_campanha_membros_oficiais_por_id(
    client: FlaskClient, seed_campanha_membros_oficiais, membro_token
):
    campanha = seed_campanha_membros_oficiais
    response = client.get(
        f'{ROTA}/{campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_buscar_campanha_membros_cadastro_por_id(
    client: FlaskClient, seed_campanha_cadastro, membro_token
):
    response = client.get(
        f'{ROTA}/{seed_campanha_cadastro.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_buscar_campanha_nao_existente(client: FlaskClient, membro_token):
    campanha_nao_existente_id = uuid.uuid4()

    response = client.get(
        f'{ROTA}/{campanha_nao_existente_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    assert response.get_json() == [{'msg': 'Campanha não encontrada'}]
