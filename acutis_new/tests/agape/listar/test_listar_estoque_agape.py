from http import HTTPStatus

from flask.testing import FlaskClient

ENDPOINT = '/api/agape/listar-itens'


def test_listar_item_estoque_agape(
    client: FlaskClient, seed_item_estoque_agape, membro_token
):
    response = client.get(
        ENDPOINT, headers={'Authorization': f'Bearer {membro_token}'}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json

    # Validar estrutura de paginação na resposta
    assert 'resultados' in data

    resultado = data['resultados'][0]

    assert 'id' in resultado
    assert 'item' in resultado
    assert 'quantidade' in resultado

    assert resultado['id'] == str(seed_item_estoque_agape.id)
    assert resultado['item'] == seed_item_estoque_agape.item
    assert resultado['quantidade'] == seed_item_estoque_agape.quantidade
