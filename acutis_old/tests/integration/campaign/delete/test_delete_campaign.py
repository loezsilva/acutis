from http import HTTPStatus
from flask.testing import FlaskClient
from builder import db
from models.campanha import Campanha


def test_registers_of_campaign_success(
    test_client: FlaskClient, seed_admin_user_token, seed_campaign
) -> None:

    response = test_client.delete(
        f"/campaigns/{seed_campaign.id}",
        headers=seed_admin_user_token,
    )
    assert response.status_code == HTTPStatus.OK

    data = response.get_json()

    assert data["msg"] == "Campanha deletada com sucesso!"
