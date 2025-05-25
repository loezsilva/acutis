from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

faker = Faker()


def test_registrar_pre_cadastro_vocacional(client: FlaskClient):
    data_request = {
        'nome': faker.name(),
        'email': faker.email(),
        'telefone': faker.phone_number(),
        'genero': faker.random_element(['masculino', 'feminino']),
        'pais': faker.country(),
    }

    response = client.post(
        '/api/vocacional/registrar-pre-cadastro', json=data_request
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.get_json() == {
        'msg': 'Pré-cadastro realizado com sucesso!'
    }


def test_registrar_pre_cadastro_email_ja_registrado(
    client: FlaskClient, seed_pre_cadastro_vocacional_pendentes
):
    vocacional, _ = seed_pre_cadastro_vocacional_pendentes[0]

    data_request = {
        'nome': faker.name(),
        'email': vocacional.email,
        'telefone': faker.phone_number(),
        'genero': faker.random_element(['masculino', 'feminino']),
        'pais': faker.country(),
    }

    response = client.post(
        '/api/vocacional/registrar-pre-cadastro', json=data_request
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.get_json() == [{'msg': 'Email já cadastrado'}]
