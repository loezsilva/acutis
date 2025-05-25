from http import HTTPStatus
import json
from faker import Faker
from flask.testing import FlaskClient

faker = Faker("pt-BR")


def test_register_cadastro_vocacional_brasileiro(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_aproved
):

    pre_cadastro_vocacional, etapa = seed_pre_cadastro_vocacional_aproved

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58497023005",
        "pais": "brasil",
        "data_nascimento": "1980-01-12",
        "cep": "01001000",
        "rua": "Rua das Flores",
        "numero": faker.random_int(),
        "complemento": "Apto 301",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
    }

    response_success = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_success.status_code == HTTPStatus.OK
    data = response_success.get_json()
    assert data["msg"] == "Cadastro vocacional realizado com sucesso."

    # tentativa de se cadastrar novamente

    response_conflict = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Cadastro vocacional já registrado anteriormente."


def test_register_cadastro_vocacional_brasileiro_conflito(
    test_client: FlaskClient, seed_cadastro_vocacional_aprovado
):

    pre_cadastro_vocacional, etapa = seed_cadastro_vocacional_aprovado

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58497023005",
        "pais": "brasil",
        "data_nascimento": "1980-01-12",
        "cep": "01001000",
        "rua": "Rua das Flores",
        "numero": faker.random_int(),
        "complemento": "Apto 301",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
    }

    response_conflict = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Cadastro vocacional já registrado anteriormente."


def test_register_cadastro_vocacional_brasileiro_reprovado(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_reproved
):

    pre_cadastro_vocacional, etapa = seed_pre_cadastro_vocacional_reproved

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58497023005",
        "pais": "brasil",
        "data_nascimento": "1980-01-12",
        "cep": "01001000",
        "rua": "Rua das Flores",
        "numero": faker.random_int(),
        "complemento": "Apto 301",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
    }

    response_success = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_success.status_code == HTTPStatus.CONFLICT
    data = response_success.get_json()
    assert (
        data["error"]
        == "Não é possível prosseguir pois seu cadastrado foi marcado como recusado anteriomente."
    )


def test_register_cadastro_vocacional_brasileiro_nao_aprovado(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_pendentes
):

    pre_cadastro_vocacional = seed_pre_cadastro_vocacional_pendentes[0][0]

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58497023005",
        "pais": "brasil",
        "data_nascimento": "1980-01-12",
        "cep": "01001000",
        "rua": "Rua das Flores",
        "numero": faker.random_int(),
        "complemento": "Apto 301",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
    }

    response_success = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_success.status_code == HTTPStatus.CONFLICT
    data = response_success.get_json()
    assert data["error"] == "É necessário ter o pre_cadastro aprovado para continuar."


def test_register_cadastro_vocacional_brasileiro_desistencia(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_desistencia
):

    pre_cadastro_vocacional, etapa = seed_pre_cadastro_vocacional_desistencia

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58497023005",
        "pais": "brasil",
        "data_nascimento": "1980-01-12",
        "cep": "01001000",
        "rua": "Rua das Flores",
        "numero": faker.random_int(),
        "complemento": "Apto 301",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
    }

    response_success = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_success.status_code == HTTPStatus.CONFLICT
    data = response_success.get_json()
    assert (
        data["error"]
        == "Não é possível prosseguir pois encontramos um registro de desistência no seu processo vocacional."
    )


def test_register_cadastro_vocacional_brasileiro_cpf_ja_cadastrado(
    test_client: FlaskClient,
    seed_pre_cadastro_vocacional_aproved,
    seed_cadastro_vocacional_pendente,
):

    pre_cadastro_vocacional, etapa = seed_pre_cadastro_vocacional_aproved

    cadastro_vocacional = seed_cadastro_vocacional_pendente

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": cadastro_vocacional.documento_identidade,
        "pais": "brasil",
        "data_nascimento": "1980-01-12",
        "cep": "01001000",
        "rua": "Rua das Flores",
        "numero": faker.random_int(),
        "complemento": "Apto 301",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
    }

    response_conflict_cpf = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_conflict_cpf.status_code == HTTPStatus.CONFLICT
    data = response_conflict_cpf.get_json()
    assert data["error"] == "Número do documento de identificação já cadastrado."


def test_register_cadastro_vocacional_estrangeriro_com_campos_de_endereco(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_aproved
):

    pre_cadastro_vocacional, etapa = seed_pre_cadastro_vocacional_aproved

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58497023424242005",
        "pais": "uruguao",
        "data_nascimento": "1980-01-12",
        "rua": "Rua das Flores",
        "numero": faker.random_int(),
        "complemento": "Apto 301",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
        "detalhe_estrangeiro": "Rua gringa de cima",
    }

    response_success = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_success.status_code == HTTPStatus.OK
    data = response_success.get_json()
    assert data["msg"] == "Cadastro vocacional realizado com sucesso."

    # tentativa de se cadastrar novamente

    response_conflict = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Cadastro vocacional já registrado anteriormente."


def test_register_cadastro_vocacional_estrangeriro_com_campos_de_endereco_conflito(
    test_client: FlaskClient, seed_cadastro_vocacional_aprovado
):

    pre_cadastro_vocacional, etapa = seed_cadastro_vocacional_aprovado

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58497023424242005",
        "pais": "uruguao",
        "data_nascimento": "1980-01-12",
        "rua": "Rua das Flores",
        "numero": faker.random_int(),
        "complemento": "Apto 301",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
        "detalhe_estrangeiro": "Rua gringa de cima",
    }

    response_conflict = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Cadastro vocacional já registrado anteriormente."


def test_register_cadastro_vocacional_estrangeriro_apenas_detalhe_estrangeiro(
    test_client: FlaskClient, seed_pre_cadastro_vocacional_aproved
):

    pre_cadastro_vocacional, etapa = seed_pre_cadastro_vocacional_aproved

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58442005",
        "pais": "uruguao",
        "data_nascimento": "1980-01-12",
        "detalhe_estrangeiro": "Rua gringa de cima",
    }

    response_success = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_success.status_code == HTTPStatus.OK
    data = response_success.get_json()
    assert data["msg"] == "Cadastro vocacional realizado com sucesso."

    # tentativa de se cadastrar novamente

    response_conflict = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Cadastro vocacional já registrado anteriormente."


def test_register_cadastro_vocacional_estrangeriro_apenas_detalhe_estrangeiro(
    test_client: FlaskClient, seed_cadastro_vocacional_aprovado
):

    pre_cadastro_vocacional, etapa = seed_cadastro_vocacional_aprovado

    data_create_register = {
        "fk_usuario_vocacional_id": pre_cadastro_vocacional.id,
        "documento_identidade": "58442005",
        "pais": "uruguao",
        "data_nascimento": "1980-01-12",
        "detalhe_estrangeiro": "Rua gringa de cima",
    }

    response_conflict = test_client.post(
        "/vocacional/registrar-cadastro-vocacional", json=data_create_register
    )

    assert response_conflict.status_code == HTTPStatus.CONFLICT
    data_conflict = response_conflict.get_json()
    assert data_conflict["error"] == "Cadastro vocacional já registrado anteriormente."
