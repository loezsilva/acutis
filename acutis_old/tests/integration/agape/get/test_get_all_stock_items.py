from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_all_stock_items_success(
    test_client: FlaskClient, seed_admin_user_token, seed_stock_items
):
    response = test_client.get(
        "/agape/listar-itens-estoque", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["estoques"]) > 0
