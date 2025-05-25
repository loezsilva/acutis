from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_all_members_by_family_id_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_family_members
):
    _, family = seed_agape_family_members
    total = 10

    response = test_client.get(
        f"/agape/listar-membros/{family.id}", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["membros"]) == total


def test_get_all_members_by_family_id_pagination_should_return_5_members(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_family_members
):
    _, family = seed_agape_family_members
    total = 5

    response = test_client.get(
        f"/agape/listar-membros/{family.id}?page=1&per_page=5",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["membros"]) == total
