from flask.testing import FlaskClient


def test_forgot_password_success(test_client: FlaskClient, create_test_user):
    user = create_test_user

    payload = {"email": user.email}

    response = test_client.post("/auth/forgot-password", json=payload)

    assert response.status_code == 200
    assert response.json["msg"] == "Email enviado com sucesso."
