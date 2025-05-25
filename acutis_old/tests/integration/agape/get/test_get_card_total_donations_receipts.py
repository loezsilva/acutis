from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_card_total_donations_receipts_success(
    test_client: FlaskClient, seed_admin_user_token, seed_stock_statistics
):
    _, familia, _ = seed_stock_statistics

    response = test_client.get(
        f"/agape/card-total-recebimentos/{familia.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"total_itens_recebidos": "100 Itens recebidos"}


def test_get_card_total_donations_receipts_error_family_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    response = test_client.get(
        "/agape/card-total-recebimentos/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Familia não encontrada."}


def test_get_card_total_donations_receipts_error_family_deleted(
    test_client: FlaskClient, seed_admin_user_token, seed_family_deleted
):
    familia = seed_family_deleted
    response = test_client.get(
        f"/agape/card-total-recebimentos/{familia.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Familia não encontrada."}
