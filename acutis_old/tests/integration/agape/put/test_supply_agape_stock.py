from http import HTTPStatus
from flask.testing import FlaskClient


def test_supply_agape_stock_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_stock
):
    stock = seed_agape_stock
    payload = {"quantidade": 10}

    response = test_client.put(
        f"/agape/abastecer-estoque/{stock.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"msg": "Estoque abastecido com sucesso."}


def test_supply_agape_stock_error_stock_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    payload = {"quantidade": 10}

    response = test_client.put(
        "/agape/abastecer-estoque/999",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Item do estoque não encontrado."}
