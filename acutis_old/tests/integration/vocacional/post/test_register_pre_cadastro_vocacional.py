from http import HTTPStatus
from flask.testing import FlaskClient
from faker import Faker

faker = Faker()


def test_register_pre_cadastro_vocacional(test_client: FlaskClient):

    data_request = {
        "nome": faker.name(),
        "email": faker.email(),
        "telefone": faker.phone_number(),
        "genero": faker.random_element(["masculino", "feminino"]),
        "pais": faker.country(),
    }

    response = test_client.post("/vocacional/registrar-pre-cadastro", json=data_request)

    assert response.status_code == HTTPStatus.CREATED
    assert response.get_json() == {"msg": "Pré-cadastro realizado com sucesso!"}


def test_register_pre_cadastro_email_ja_registrado(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_pendentes
):

    vocacional, etapa = seed_pre_cadastro_vocacional_pendentes[0]

    data_request = {
        "nome": faker.name(),
        "email": vocacional.email,
        "telefone": faker.phone_number(),
        "genero": faker.random_element(["masculino", "feminino"]),
        "pais": faker.country(),
    }

    response = test_client.post("/vocacional/registrar-pre-cadastro", json=data_request)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json() == {"error": "Email já cadastrado"}
