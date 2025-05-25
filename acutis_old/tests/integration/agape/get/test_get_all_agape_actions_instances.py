from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_all_agape_actions_instances_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
) -> None:
    response = test_client.get(
        "/agape/listar-ciclos-acoes-agape", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["ciclos"]) > 0
