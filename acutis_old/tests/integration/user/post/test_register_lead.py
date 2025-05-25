from http import HTTPStatus
from io import BytesIO
from flask.testing import FlaskClient

from models.foto_leads import FotoLeads
from models.users_imports import UsersImports
from builder import db
from tests.factories import AcaoLeadFactory, LeadFactory


def test_create_lead_success(test_client: FlaskClient, seed_new_lead_action):

    action = seed_new_lead_action

    lead_data = {
        "nome": "Usuário Teste",
        "email": "teste@headers.com.br",
        "telefone": "11987654321",
        "origem": action.id,
        "intencao": "Participar da campanha",
        "foto": (BytesIO(b"fake image data"), "foto.jpg"),
    }

    response = test_client.post(
        "/users/create-lead",
        content_type="multipart/form-data",
        data=lead_data,
    )

    assert response.status_code == 201
    assert response.json["msg"] == "Pré cadastro realizado com sucesso!"

    lead = UsersImports.query.filter_by(email=lead_data["email"]).first()
    assert lead is not None
    assert lead.nome == lead_data["nome"]
    assert lead.phone == lead_data["telefone"]
    assert lead.origem_cadastro == lead_data["origem"]
    assert lead.intencao == lead_data["intencao"]

    lead_photo = FotoLeads.query.filter_by(fk_user_import_id=lead.id).first()
    assert lead_photo is not None


def test_register_lead_already_registered_success(
    test_client: FlaskClient, seed_new_lead_already_registered
):

    lead, photo_lead = seed_new_lead_already_registered

    updated_data = {
        "nome": "Usuário Atualizado",
        "email": lead.email,
        "telefone": "11999999999",
        "origem": lead.origem_cadastro,
        "intencao": "Nova intenção",
        "foto": (BytesIO(b"new fake image data"), "nova_foto.jpg"),
    }

    response = test_client.post(
        "/users/create-lead",
        content_type="multipart/form-data",
        data=updated_data,
    )

    assert response.status_code == 201
    assert response.json["msg"] == "Pré cadastro realizado com sucesso!"

    db.session.refresh(lead)
    assert lead is not None
    assert lead.nome == updated_data["nome"]
    assert lead.phone == updated_data["telefone"]
    assert lead.intencao == updated_data["intencao"]

    db.session.refresh(photo_lead)
    assert photo_lead is not None
    assert photo_lead.data_download is None
    assert photo_lead.user_download is None


def test_register_lead_update_without_photo(test_client: FlaskClient):
    acao_lead = AcaoLeadFactory(preenchimento_foto=True)
    db.session.add(acao_lead)
    db.session.flush()

    lead = LeadFactory(origem_cadastro=acao_lead.id)
    db.session.add(lead)
    db.session.commit()

    lead_data = {
        "nome": "nome atualizado",
        "email": lead.email,
        "telefone": "85999887766",
        "origem": acao_lead.id,
        "intencao": "intencao de teste atualizada",
        "foto": (BytesIO(b"test image data"), "foto_teste.jpg"),
    }

    response = test_client.post(
        "/users/create-lead",
        content_type="multipart/form-data",
        data=lead_data,
    )

    assert response.status_code == 201
    assert response.json["msg"] == "Pré cadastro realizado com sucesso!"

    db.session.refresh(lead)
    assert lead is not None
    assert lead.nome == (lead_data["nome"]).title()
    assert lead.phone == lead_data["telefone"]
    assert lead.intencao == lead_data["intencao"]

    lead_foto = FotoLeads.query.filter_by(
        fk_action_lead_id=acao_lead.id, fk_user_import_id=lead.id
    ).first()
    assert lead_foto is not None
    assert lead_foto.foto is not None


def test_register_lead_error_action_not_found(test_client: FlaskClient):
    lead_data = {
        "nome": "Usuário Teste",
        "email": "teste@headers.com.br",
        "telefone": "11987654321",
        "origem": 9999,
        "intencao": "Participar da campanha",
        "foto": (BytesIO(b"fake image data"), "foto.jpg"),
    }

    response = test_client.post(
        "/users/create-lead",
        content_type="multipart/form-data",
        data=lead_data,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ação não encontrada."}


def test_register_lead_error_action_status_false(test_client: FlaskClient):
    action = AcaoLeadFactory(status=False)
    db.session.add(action)
    db.session.commit()

    lead_data = {
        "nome": "Usuário Teste",
        "email": "teste@headers.com.br",
        "telefone": "11987654321",
        "origem": action.id,
        "intencao": "Participar da campanha",
        "foto": (BytesIO(b"fake image data"), "foto.jpg"),
    }

    response = test_client.post(
        "/users/create-lead",
        content_type="multipart/form-data",
        data=lead_data,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": "Esta ação não está ativa para receber novos cadastros."
    }
