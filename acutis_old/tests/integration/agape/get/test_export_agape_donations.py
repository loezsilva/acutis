from http import HTTPStatus
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token


def test_export_agape_donations_success(
    test_client: FlaskClient, seed_admin_user_token
):
    response = test_client.get(
        "/agape/exportar-doacoes-beneficiados/1",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert "url" in response.json


def test_export_agape_donations_error_forbidden(
    test_client: FlaskClient, seed_user_with_dependencies
):
    user, _, _, _ = seed_user_with_dependencies
    token = create_access_token(identity=user.id)

    response = test_client.get(
        "/agape/exportar-doacoes-beneficiados/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json == {
        "error": "Você não tem permissão para realizar esta ação."
    }
