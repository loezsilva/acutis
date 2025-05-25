import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_deletar_item_sucesso(
    client: FlaskClient, seed_item_estoque_agape, membro_token
):
    response = client.delete(
        f'/api/agape/deletar-item/{seed_item_estoque_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_erro_deletar_item_inexistente(client: FlaskClient, membro_token):
    response = client.delete(
        f'/api/agape/deletar-item/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'msg' in response.json[0]
