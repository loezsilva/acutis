from flask.testing import FlaskClient

from models.perfil import Perfil
from builder import db
from models.permissao_menu import PermissaoMenu


def test_register_profile_success(
    test_client: FlaskClient, seed_admin_user_token
):
    payload = {"nome": "Perfil de teste", "status": True, "super_perfil": True}

    response = test_client.post(
        "/administradores/cadastrar-perfil",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Perfil cadastrado com sucesso!"

    created_profile = (
        db.session.query(Perfil).filter_by(nome="Perfil de teste").first()
    )
    assert created_profile is not None
    assert created_profile.nome == "Perfil de teste"
    assert created_profile.status == True
    assert created_profile.super_perfil == True

    created_permissions = (
        db.session.query(PermissaoMenu)
        .filter_by(fk_perfil_id=created_profile.id)
        .all()
    )
    assert len(created_permissions) > 0

    db.session.delete(created_profile)
    db.session.commit()
