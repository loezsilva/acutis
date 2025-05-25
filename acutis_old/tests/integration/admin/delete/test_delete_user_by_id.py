from flask.testing import FlaskClient
from builder import db


def test_delete_user_success(
    test_client: FlaskClient,
    seed_user_with_dependencies,
    seed_admin_user_token,
):
    user, _, _, pedido = seed_user_with_dependencies

    response = test_client.delete(
        f"/administradores/deletar-usuario/{user.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Usuário deletado com sucesso."

    db.session.refresh(user)
    assert user.deleted_at is not None

    db.session.refresh(pedido)
    assert pedido.anonimo is True
