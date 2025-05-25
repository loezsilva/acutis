import io
import json
from faker import Faker
from flask.testing import FlaskClient
from builder import db
from models.actions_leads import ActionsLeads

faker = Faker("pt_BR")


def test_register_action_success(
    test_client: FlaskClient, seed_admin_user_token
):
    nome_acao = faker.name()

    payload = {
        "data": json.dumps(
            {
                "nome": nome_acao,
                "titulo": "Ajude a Comunidade",
                "descricao": "Campanha para arrecadação de doações.",
                "status": True,
                "preenchimento_foto": True,
                "label_foto": "Banner Campanha",
            }
        )
    }

    banner = (io.BytesIO(b"fake_image_data_banner"), "banner.jpg")
    background = (io.BytesIO(b"fake_image_data_background"), "background.jpg")

    response = test_client.post(
        "/administradores/cadastrar-acao",
        data={**payload, "banner": banner, "background": background},
        headers=seed_admin_user_token,
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Ação cadastrada com sucesso!"

    action = db.session.query(ActionsLeads).filter_by(nome=nome_acao).first()
    assert action is not None
    assert action.nome == nome_acao
    assert action.titulo == "Ajude a Comunidade"
    assert action.descricao == "Campanha para arrecadação de doações."
    assert action.status == True
    assert action.preenchimento_foto is True
    assert action.label_foto == "Banner Campanha"
    assert action.banner is not None
    assert action.background is not None
