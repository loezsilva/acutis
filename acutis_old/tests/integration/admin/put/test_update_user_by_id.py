from flask.testing import FlaskClient

from builder import db


def test_update_user_by_id_success(
    test_client: FlaskClient, seed_user_to_admin_update, seed_admin_user_token
):
    user, clifor = seed_user_to_admin_update

    payload = {
        "pais": "brasil",
        "nome": "Updated User",
        "telefone": "(11) 91234-5678",
        "email": "updatedusertest@headers.com.br",
    }

    response = test_client.put(
        f"/administradores/editar-usuario/{user.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Usuário atualizado com sucesso"

    db.session.refresh(user)
    assert user.nome == "Updated User"
    assert user.email == "updatedusertest@headers.com.br"

    db.session.refresh(clifor)
