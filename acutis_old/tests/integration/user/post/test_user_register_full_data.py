import io
import json
from faker import Faker
from flask.testing import FlaskClient
import pytest

faker = Faker("pt_BR")


@pytest.mark.skip(reason="Teste pendente de atualizacao")
def test_register_new_user_full_data_success(test_client: FlaskClient):
    payload = {
        "usuario": {
            "data_nascimento": faker.date(),
            "email": faker.email(domain="hotmail.com"),
            "nome": "Maria Luísa Cunha",
            "nome_social": "Maria Luísa Cunha",
            "numero_documento": "89.780.793/0001-12",
            "pais": "brasil",
            "password": "#Test1234",
            "tipo_documento": "cnpj",
            "telefone": "11999999999",
            "sexo": "feminino",
        },
        "endereco": {
            "bairro": "Nova Brasília",
            "cep": "41351280",
            "cidade": "Salvador",
            "estado": "BA",
            "numero": "21",
            "rua": "Caminho",
        },
    }

    avatar = (io.BytesIO(b"fake_image_data"), "avatar.jpg")

    response = test_client.post(
        "/users/cadastrar-usuario-completo",
        data={
            "data": json.dumps(payload),
            "image": avatar,
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {"msg": "Usuário cadastrado com sucesso."}


@pytest.mark.skip(reason="Teste pendente de atualizacao")
def test_register_deleted_user_full_data_success(
    test_client: FlaskClient, seed_register_deleted_user_full_data
):
    payload = {
        "usuario": {
            "data_nascimento": "2000-04-14",
            "email": "debora-vieira72@hotmail.com",
            "nome": "Débora Clara Lorena Vieira",
            "nome_social": "debrinha clarinha",
            "numero_documento": "37000086270",
            "pais": "brasil",
            "password": "#Debora1234",
            "tipo_documento": "cpf",
            "telefone": "11999999999",
            "sexo": "feminino",
        },
        "endereco": {
            "bairro": "Nova Brasília",
            "cep": "41351280",
            "cidade": "Salvador",
            "estado": "BA",
            "numero": "21",
            "rua": "Caminho",
        },
    }

    avatar = (io.BytesIO(b"fake_image_data"), "avatar.jpg")

    response = test_client.post(
        "/users/cadastrar-usuario-completo",
        data={
            "data": json.dumps(payload),
            "image": avatar,
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {"msg": "Usuário cadastrado com sucesso."}


@pytest.mark.skip(reason="Teste pendente de atualizacao")
def test_register_anonymous_user_full_data_success(
    test_client: FlaskClient, seed_register_anonymous_user
):

    payload = {
        "usuario": {
            "data_nascimento": faker.date(),
            "email": faker.email(domain="hotmail.com"),
            "nome": "Maria Luísa Cunha",
            "nome_social": "Maria Luísa Cunha",
            "numero_documento": faker.cnpj(),
            "pais": "brasil",
            "password": "#Test1234",
            "tipo_documento": "cnpj",
            "telefone": "11999999999",
            "sexo": "feminino",
        },
        "endereco": {
            "bairro": "Nova Brasília",
            "cep": "41351280",
            "cidade": "Salvador",
            "estado": "BA",
            "numero": "21",
            "rua": "Caminho",
        },
    }

    avatar = (io.BytesIO(b"fake_image_data"), "avatar.jpg")

    response = test_client.post(
        "/users/cadastrar-usuario-completo",
        data={
            "data": json.dumps(payload),
            "image": avatar,
        },
    )

    assert response.status_code == 201
    assert response.get_json() == {"msg": "Usuário cadastrado com sucesso."}
