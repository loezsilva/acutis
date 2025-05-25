from flask.testing import FlaskClient
from models.perfil import Perfil
from models.permissao_usuario import PermissaoUsuario
from builder import db


def test_update_user_permission_success(
    test_client: FlaskClient, seed_admin_user_token, seed_test_user
):

    user = seed_test_user
    admin = Perfil.query.filter_by(nome="Administrador").first()
    benefector = Perfil.query.filter_by(nome="Benfeitor").first()
    user_permission = PermissaoUsuario(
        fk_usuario_id=user.id, fk_perfil_id=benefector.id, usuario_criacao=0
    )
    db.session.add(user_permission)
    db.session.commit()

    payload = {"fk_perfil_id": admin.id}

    response = test_client.put(
        f"/administradores/editar-usuario-perfil/{user.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Permissão de usuário atualizada com sucesso!"
    db.session.refresh(user_permission)
    assert user_permission.fk_perfil_id == admin.id

    db.session.delete(user_permission)
    db.session.commit()
