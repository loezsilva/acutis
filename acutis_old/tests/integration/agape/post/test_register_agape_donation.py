from http import HTTPStatus
from flask.testing import FlaskClient


def test_register_agape_donation_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_register_agape_donation,
):
    familia_agape, instancia_acao_agape, item_instancia_agape = (
        seed_register_agape_donation
    )

    payload = {
        "fk_familia_agape_id": familia_agape.id,
        "fk_instancia_acao_agape_id": instancia_acao_agape.id,
        "doacoes": [
            {
                "fk_item_instancia_agape_id": item_instancia_agape.id,
                "quantidade": 10,
            }
        ],
    }

    response = test_client.post(
        "/agape/registrar-doacao",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json["msg"] == "Doação registrada com sucesso."
    assert response.json["fk_doacao_agape_id"] is not None


def test_register_agape_donation_error_family_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_register_agape_donation,
):
    _, instancia_acao_agape, item_instancia_agape = (
        seed_register_agape_donation
    )

    payload = {
        "fk_familia_agape_id": 999,
        "fk_instancia_acao_agape_id": instancia_acao_agape.id,
        "doacoes": [
            {
                "fk_item_instancia_agape_id": item_instancia_agape.id,
                "quantidade": 10,
            }
        ],
    }

    response = test_client.post(
        "/agape/registrar-doacao",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Família não encontrada."}


def test_register_agape_donation_error_family_deleted(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_family_deleted,
):
    familia_agape = seed_family_deleted

    payload = {
        "fk_familia_agape_id": familia_agape.id,
        "fk_instancia_acao_agape_id": 1,
        "doacoes": [
            {
                "fk_item_instancia_agape_id": 1,
                "quantidade": 10,
            }
        ],
    }

    response = test_client.post(
        "/agape/registrar-doacao",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Família não encontrada."}


def test_register_agape_donation_error_family_inactive(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_family_inactive,
):
    familia_agape = seed_family_inactive

    payload = {
        "fk_familia_agape_id": familia_agape.id,
        "fk_instancia_acao_agape_id": 1,
        "doacoes": [
            {
                "fk_item_instancia_agape_id": 1,
                "quantidade": 10,
            }
        ],
    }

    response = test_client.post(
        "/agape/registrar-doacao",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": "Familia com status inativo para receber doações."
    }


def test_register_agape_donation_error_instance_status(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_instance,
):
    familia_agape, instancia_acao_agape = seed_agape_action_instance

    payload = {
        "fk_familia_agape_id": familia_agape.id,
        "fk_instancia_acao_agape_id": instancia_acao_agape.id,
        "doacoes": [
            {
                "fk_item_instancia_agape_id": 1,
                "quantidade": 10,
            }
        ],
    }

    response = test_client.post(
        "/agape/registrar-doacao",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": "Status do ciclo está indisponível para realizar doação."
    }


def test_register_agape_donation_error_insufficient_stock(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_register_agape_donation,
):
    familia_agape, instancia_acao_agape, item_instancia_agape = (
        seed_register_agape_donation
    )

    payload = {
        "fk_familia_agape_id": familia_agape.id,
        "fk_instancia_acao_agape_id": instancia_acao_agape.id,
        "doacoes": [
            {
                "fk_item_instancia_agape_id": item_instancia_agape.id,
                "quantidade": 1000,
            }
        ],
    }

    response = test_client.post(
        "/agape/registrar-doacao",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": "O ciclo da ação possui itens com quantidades insuficientes para realizar esta doação."
    }
