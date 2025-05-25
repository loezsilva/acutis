from http import HTTPStatus

from flask.testing import FlaskClient


def test_listar_membros_oficiais_sucesso(
    client: FlaskClient, seed_membros_oficial, membro_token
):
    response = client.get(
        '/api/admin/membros-oficiais/listar',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_listar_membros_oficiais_nao_autorizado(
    client: FlaskClient, seed_membros_oficial
):
    response = client.get(
        '/api/admin/membros-oficiais/listar',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
