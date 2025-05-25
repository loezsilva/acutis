from http import HTTPStatus
from flask.testing import FlaskClient

from models.schemas.agape.get.get_family_address_by_id import (
    GetFamilyAddressByIdResponse,
)


def test_get_family_address_by_id_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_family
):
    address, family = seed_agape_family

    response = test_client.get(
        f"/agape/buscar-endereco-familia/{family.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert (
        response.get_json()
        == GetFamilyAddressByIdResponse.from_orm(address).dict()
    )


def test_get_family_address_error_family_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    response = test_client.get(
        "/agape/buscar-endereco-familia/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == {"error": "Familia não encontrada."}
