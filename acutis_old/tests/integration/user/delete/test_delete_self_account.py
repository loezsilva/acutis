from flask_jwt_extended import create_access_token
from flask.testing import FlaskClient
from builder import db


def test_delete_self_account_success(
    test_client: FlaskClient, seed_user_with_dependencies
):
    user, _, _, pedido = seed_user_with_dependencies

    access_token = create_access_token(identity=user.id)

    response = test_client.delete(
        "/users/delete-self-account",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Sua conta foi excluída com sucesso."

    db.session.refresh(user)
    assert user.deleted_at is not None

    db.session.refresh(pedido)
    assert pedido.anonimo is True
