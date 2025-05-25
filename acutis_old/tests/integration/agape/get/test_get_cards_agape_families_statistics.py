from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_cards_agape_families_statistics_success(
    test_client: FlaskClient, seed_admin_user_token, seed_families_statistics
):
    response = test_client.get(
        "/agape/cards-estatisticas-familias-agape",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["familias_cadastradas"] == "6 - Famílias ativas"
    assert response.json["familias_ativas"] == "6 - 60%"
    assert response.json["familias_inativas"] == "4 - 40%"
    assert response.json["membros_por_familia"] == "5.0 pessoas"
    assert response.json["renda_media"] == "3.3 Salários minimos"
