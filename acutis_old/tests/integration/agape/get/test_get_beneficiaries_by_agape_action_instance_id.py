from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_beneficiaries_by_agape_action_instance_id_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
):
    instancia_acao_agape, _, _, _, _ = seed_get_beneficiaries_and_items

    response = test_client.get(
        f"/agape/listar-beneficiarios/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["total"] == 1
    assert len(response.json["beneficiarios"]) == 1
    assert len(response.json["beneficiarios"][0]["recibos"]) == 2
