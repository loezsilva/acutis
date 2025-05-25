from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_all_agape_actions_names_success(
    test_client: FlaskClient, seed_admin_user_token, seed_many_agape_actions
):
    response = test_client.get(
        "/agape/listar-nomes-acoes-agape", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["acoes_agape"]) > 0
