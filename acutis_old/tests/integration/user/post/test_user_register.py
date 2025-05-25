from flask.testing import FlaskClient
from models.perfil import Perfil
from models.usuario import Usuario
from builder import db


def test_register_new_user_success(test_client: FlaskClient):
    payload = {
        "email": "neville.guimaraes@headers.com.br",
        "nome": "Gary Neville",
        "numero_documento": "53794004000",
        "pais": "brasil",
        "password": "Test1234@1234",
        "tipo_documento": "cpf",
    }

    response = test_client.post(
        "/users/register", json=payload, content_type="application/json"
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Usuário cadastrado com sucesso."
    user = Usuario.query.filter_by(email=payload["email"]).first()
    assert user is not None
    assert user.nome == payload["nome"]
    assert user.verify_password(payload["password"]) is True


def test_register_deleted_user_success(
    test_client: FlaskClient, seed_register_deleted_user
):
    user_permission = seed_register_deleted_user

    payload = {
        "email": "testeemaildeleted@institutohesed.org.br",
        "nome": "Marcos Aurélio",
        "numero_documento": "65335887028",
        "pais": "brasil",
        "password": "Test1234@1234",
        "tipo_documento": "cpf",
    }

    response = test_client.post(
        "/users/register", json=payload, content_type="application/json"
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Usuário cadastrado com sucesso."

    db.session.refresh(user_permission)
    perfil: Perfil = Perfil.query.filter(
        Perfil.nome.ilike("Benfeitor")
    ).first()
    assert user_permission.fk_perfil_id == perfil.id


def test_register_anonymous_user_success(
    test_client: FlaskClient, seed_register_anonymous_user
):
    payload = {
        "email": "testeemailanonymous@institutohesed.org.br",
        "nome": "Yan o brabo",
        "numero_documento": "15718702000182",
        "pais": "brasil",
        "password": "Test1234@1234",
        "tipo_documento": "cnpj",
    }

    response = test_client.post(
        "/users/register", json=payload, content_type="application/json"
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Usuário cadastrado com sucesso."
