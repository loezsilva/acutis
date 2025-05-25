from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_card_agape_family_income_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_family_income
):
    familia = seed_agape_family_income

    response = test_client.get(
        f"/agape/card-renda-familiar-agape/{familia.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "renda_familiar": "5.0 Salários minimos",
        "renda_per_capta": "1.0 Salários minimos",
    }


def test_get_card_agape_family_income_error_family_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    response = test_client.get(
        "/agape/card-renda-familiar-agape/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Familia não encontrada."}


def test_get_card_agape_family_income_error_family_deleted(
    test_client: FlaskClient, seed_admin_user_token, seed_family_deleted
):
    familia = seed_family_deleted

    response = test_client.get(
        f"/agape/card-renda-familiar-agape/{familia.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Familia não encontrada."}
