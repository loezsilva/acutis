from flask.testing import FlaskClient


def test_resend_active_account_email_success(
    test_client: FlaskClient, seed_test_user, seed_admin_user_token
):
    user = seed_test_user

    response = test_client.post(
        f"/administradores/reenviar-email-ativacao-conta/{user.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Email enviado com sucesso!"
