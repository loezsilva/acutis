from flask.testing import FlaskClient
from builder import db
from utils.token_email import generate_token


def test_active_account_success(
    test_client: FlaskClient, seed_user_active_account
):
    user = seed_user_active_account

    token_active_account = generate_token(
        {"email": user.email, "campanha_origem": 16},
        salt="active_account_confirmation",
    )

    response = test_client.post(
        f"/users/active-account/{token_active_account}"
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data

    db.session.refresh(user)
    assert user.status is True
