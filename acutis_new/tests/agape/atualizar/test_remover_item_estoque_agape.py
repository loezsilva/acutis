import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_remover_item_sucesso(
    client: FlaskClient, seed_item_estoque_agape, membro_token
):
    quantidade_removida = 1
    quantidade_antiga = int(seed_item_estoque_agape.quantidade)

    response = client.put(
        f'/api/agape/remover-item/{seed_item_estoque_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={'quantidade': quantidade_removida},
    )

    response_json = response.json
    nova_quantidade = int(response_json['quantidade'])

    assert response.status_code == HTTPStatus.OK
    assert nova_quantidade == (quantidade_antiga - quantidade_removida)


def test_erro_remover_item_inexistente(client: FlaskClient, membro_token):
    response = client.put(
        f'/api/agape/remover-item/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={'quantidade': 1},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'msg' in response.json[0]


def test_erro_remover_item_quantidade_invalida(
    client: FlaskClient, seed_item_estoque_agape, membro_token
):
    response = client.put(
        f'/api/agape/remover-item/{seed_item_estoque_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
        data={'quantidade': -1},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        'a quantidade deve ser maior ou igual a 1.'
        in response.json[0]['msg'].lower()
    )
