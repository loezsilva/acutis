from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token
from builder import db


def test_change_password_success(
    test_client: FlaskClient, seed_user_with_dependencies
):
    user, _, _, _ = seed_user_with_dependencies

    access_token = create_access_token(identity=user.id)

    payload = {
        "old_password": "SenhaAntiga123",
        "new_password": "@NovaSenha456",
    }

    response = test_client.post(
        "/users/change-password",
        json=payload,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Senha alterada com sucesso."

    db.session.refresh(user)
    assert user.verify_password("@NovaSenha456") is True
