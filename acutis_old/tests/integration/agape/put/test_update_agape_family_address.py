from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

from builder import db as database
from models.schemas.agape.put.update_agape_family_address import (
    UpdateAgapeFamilyAddressRequest,
)

faker = Faker("pt-BR")


def test_update_agape_family_address_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_family
):
    db_address, db_family = seed_agape_family
    payload = {
        "bairro": "Jardim das Flores",
        "cep": "12345-678",
        "cidade": "São Paulo",
        "complemento": "Apto 101",
        "estado": "SP",
        "numero": "123",
        "ponto_referencia": "Próximo ao mercado",
        "rua": "Rua das Acácias",
    }
    address = UpdateAgapeFamilyAddressRequest.parse_obj(payload)

    response = test_client.put(
        f"/agape/editar-endereco-familia/{db_family.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"msg": "Endereço atualizado com sucesso."}

    database.session.refresh(db_address)
    assert db_address.bairro == address.bairro
    assert db_address.cep == address.cep
    assert db_address.cidade == address.cidade
    assert db_address.complemento == address.complemento
    assert db_address.estado == address.estado
    assert db_address.numero == address.numero
    assert db_address.ponto_referencia == address.ponto_referencia
    assert db_address.rua == address.rua


def test_update_agape_family_address_error_family_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    payload = {
        "bairro": "Jardim das Flores",
        "cep": "12345-678",
        "cidade": "São Paulo",
        "complemento": "Apto 101",
        "estado": "SP",
        "numero": "123",
        "ponto_referencia": "Próximo ao mercado",
        "rua": "Rua das Acácias",
    }

    response = test_client.put(
        "/agape/editar-endereco-familia/9999",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Família não encontrada."}
