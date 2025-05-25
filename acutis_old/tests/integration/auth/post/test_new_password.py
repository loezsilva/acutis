from flask.testing import FlaskClient
from builder import db
from utils.token_email import generate_token


def test_new_password_success(test_client: FlaskClient, create_test_user):
    user = create_test_user

    payload = {"new_password": "NovaSenha123!"}
    token = generate_token(user.email, salt="reset_password_confirmation")

    response = test_client.post(
        f"/auth/new-password?token={token}", json=payload
    )
    assert response.status_code == 200
    assert response.json["msg"] == "Senha alterada com sucesso."

    db.session.refresh(user)
    assert user.verify_password("NovaSenha123!") is True
