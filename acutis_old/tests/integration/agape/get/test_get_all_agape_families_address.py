from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_all_agape_families_address(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_families
):
    response = test_client.get(
        "/agape/listar-enderecos-familias-agape", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["enderecos"]) > 0
    enderecos = response.json["enderecos"][0]
    assert "bairro" in enderecos
    assert "cep" in enderecos
    assert "cidade" in enderecos
    assert "complemento" in enderecos
    assert "estado" in enderecos
    assert "latitude" in enderecos
    assert "longitude" in enderecos
    assert "numero" in enderecos
    assert "ponto_referencia" in enderecos
    assert "rua" in enderecos
