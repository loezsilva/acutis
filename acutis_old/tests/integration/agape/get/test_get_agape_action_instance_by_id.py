from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_agape_action_instance_by_id_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
):
    instancia_acao_agape, _, _, _, _ = seed_get_beneficiaries_and_items

    response = test_client.get(
        f"/agape/buscar-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["abrangencia"] == instancia_acao_agape.abrangencia
    assert "endereco" in response.json
    assert len(response.json["doacoes"]) > 0
    assert (
        response.json["fk_acao_agape_id"]
        == instancia_acao_agape.fk_acao_agape_id
    )


def test_get_agape_action_instance_by_id_error_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
):
    response = test_client.get(
        "/agape/buscar-ciclo-acao-agape/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ciclo de ação ágape não encontrado."}
