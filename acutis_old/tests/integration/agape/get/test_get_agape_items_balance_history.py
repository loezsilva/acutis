from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_agape_items_balance_history_success(
    test_client: FlaskClient, seed_admin_user_token, seed_items_balance_history
):
    response = test_client.get(
        "/agape/listar-historico-movimentacoes-agape",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["movimentacoes"]) > 0
