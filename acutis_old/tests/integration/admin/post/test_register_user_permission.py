from flask.testing import FlaskClient

from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from builder import db


def test_register_user_permission_success(
    test_client: FlaskClient, seed_admin_user_token, seed_test_user
):
    user = seed_test_user
    profile = Perfil.query.filter_by(nome="Operacional").first()

    payload = {
        "fk_usuario_id": user.id,
        "fk_perfil_id": profile.id,
    }

    response = test_client.post(
        "/administradores/cadastrar-usuario-perfil",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Permissão de usuário cadastrada com sucesso!"

    user_permission = PermissaoUsuario.query.filter_by(
        fk_usuario_id=user.id, fk_perfil_id=profile.id
    ).first()
    assert user_permission is not None
    assert user_permission.fk_usuario_id == user.id
    assert user_permission.fk_perfil_id == profile.id

    db.session.delete(user_permission)
    db.session.commit()
