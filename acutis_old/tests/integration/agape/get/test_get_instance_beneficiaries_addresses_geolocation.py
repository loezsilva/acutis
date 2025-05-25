from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_instance_beneficiaries_addresses_geolocation_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_stock_statistics,
):
    instancia_acao_agape, _, _ = seed_stock_statistics

    response = test_client.get(
        f"/agape/listar-geolocalizacoes-beneficiarios-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["ciclo_acao_agape"] is not None
    assert len(response.json["beneficiarios"]) > 0
    ciclo_acao_agape = response.json["ciclo_acao_agape"]
    assert "latitude" in ciclo_acao_agape
    assert "longitude" in ciclo_acao_agape
    assert "latitude_nordeste" in ciclo_acao_agape
    assert "longitude_nordeste" in ciclo_acao_agape
    assert "latitude_sudoeste" in ciclo_acao_agape
    assert "longitude_sudoeste" in ciclo_acao_agape
    beneficiario = response.json["beneficiarios"][0]
    assert "latitude" in beneficiario
    assert "longitude" in beneficiario


def test_get_instance_beneficiaries_addresses_geolocation_error_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
):

    response = test_client.get(
        "/agape/listar-geolocalizacoes-beneficiarios-ciclo-acao-agape/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ciclo de ação ágape não encontrado."}
