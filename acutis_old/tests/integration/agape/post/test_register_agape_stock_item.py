from http import HTTPStatus
from flask.testing import FlaskClient

from builder import db
from tests.factories import EstoqueAgapeFactory


def test_register_agape_stock_item_success(
    test_client: FlaskClient, seed_admin_user_token
):
    payload = {"item": "Cesta Básica"}
    response = test_client.post(
        "/agape/cadastrar-item-estoque",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.get_json() == {"msg": "Estoque cadastrado com sucesso."}


def test_register_agape_stock_item_error_conflict(
    test_client: FlaskClient, seed_admin_user_token
):
    item = EstoqueAgapeFactory(item="Sabão em Pó")
    db.session.add(item)
    db.session.commit()

    payload = {"item": "sabao em po"}

    response = test_client.post(
        "/agape/cadastrar-item-estoque",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": f"Item {payload['item']} já cadastrado no estoque."
    }
