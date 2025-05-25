import io
import json
from flask.testing import FlaskClient
from builder import db


def test_update_action_success(
    test_client: FlaskClient, seed_action, seed_admin_user_token
):
    action = seed_action

    payload = {
        "data": json.dumps(
            {
                "nome": "Campanha Atualizada",
                "titulo": "Novo Título da Campanha",
                "descricao": "Descrição atualizada da campanha.",
                "status": False,
                "preenchimento_foto": True,
                "label_foto": "Novo Banner Campanha",
            }
        )
    }

    new_banner = (io.BytesIO(b"new_fake_image_data_banner"), "new_banner.jpg")
    new_background = (
        io.BytesIO(b"new_fake_image_data_background"),
        "new_background.jpg",
    )

    response = test_client.put(
        f"/administradores/editar-acao/{action.id}",
        data={**payload, "banner": new_banner, "background": new_background},
        content_type="multipart/form-data",
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Ação atualizada com sucesso!"

    db.session.refresh(action)
    assert action.nome == "Campanha Atualizada"
    assert action.titulo == "Novo Título da Campanha"
    assert action.descricao == "Descrição atualizada da campanha."
    assert action.status == False
    assert action.preenchimento_foto is True
    assert action.label_foto == "Novo Banner Campanha"
    assert action.banner is not None
    assert action.background is not None
