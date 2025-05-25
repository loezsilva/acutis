from flask.testing import FlaskClient
from builder import db
from models import Perfil


def test_delete_profile_success(
    test_client: FlaskClient, seed_admin_user_token, seed_test_delete_profile
):

    user_permission, profile = seed_test_delete_profile

    response = test_client.delete(
        f"/administradores/deletar-perfil/{profile.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Perfil deletado com sucesso!"

    deleted_profile = db.session.get(Perfil, profile.id)
    assert deleted_profile is None
    db.session.refresh(user_permission)
    assert user_permission.fk_perfil_id == 2
