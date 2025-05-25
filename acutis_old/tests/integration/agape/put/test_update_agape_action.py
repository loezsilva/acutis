from http import HTTPStatus
from flask.testing import FlaskClient


def test_update_agape_action_success(
    test_client: FlaskClient, seed_admin_user_token, seed_update_agape_action
):
    instancia_acao_agape, itens = seed_update_agape_action

    payload = {
        "endereco": {
            "cep": "12345-678",
            "rua": "Rua das Acácias",
            "bairro": "Jardim das Flores",
            "cidade": "São Paulo",
            "estado": "SP",
            "numero": "123",
            "complemento": "Apto 101",
        },
        "doacoes": [
            {
                "fk_estoque_agape_id": itens[0].id,
                "quantidade": itens[0].quantidade,
            },
            {
                "fk_estoque_agape_id": itens[1].id,
                "quantidade": itens[1].quantidade,
            },
            {
                "fk_estoque_agape_id": itens[2].id,
                "quantidade": itens[2].quantidade,
            },
        ],
        "abrangencia": "sem_restricao",
    }

    response = test_client.put(
        f"/agape/editar-ciclo-acao-agape/{instancia_acao_agape.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"msg": "Ciclo da ação atualizado com sucesso."}


def test_update_agape_action_error_instance_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    payload = {
        "endereco": {
            "cep": "12345-678",
            "rua": "Rua das Acácias",
            "bairro": "Jardim das Flores",
            "cidade": "São Paulo",
            "estado": "SP",
            "numero": "123",
            "complemento": "Apto 101",
        },
        "doacoes": [
            {
                "fk_estoque_agape_id": 1,
                "quantidade": 1,
            },
        ],
        "abrangencia": "cidade",
    }

    response = test_client.put(
        "/agape/editar-ciclo-acao-agape/9999",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ciclo da ação não encontrado."}


def test_update_agape_action_error_instance_already_started(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_instance_started,
):
    instancia_acao_agape = seed_agape_action_instance_started

    payload = {
        "endereco": {
            "cep": "12345-678",
            "rua": "Rua das Acácias",
            "bairro": "Jardim das Flores",
            "cidade": "São Paulo",
            "estado": "SP",
            "numero": "123",
            "complemento": "Apto 101",
        },
        "doacoes": [
            {
                "fk_estoque_agape_id": 1,
                "quantidade": 1,
            },
        ],
        "abrangencia": "estado",
    }

    response = test_client.put(
        f"/agape/editar-ciclo-acao-agape/{instancia_acao_agape.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": "Somentes ciclos nao iniciados podem ser atualizados."
    }


def test_update_agape_action_error_insufficient_stock(
    test_client: FlaskClient, seed_admin_user_token, seed_update_agape_action
):
    instancia_acao_agape, itens = seed_update_agape_action

    payload = {
        "endereco": {
            "cep": "12345-678",
            "rua": "Rua das Acácias",
            "bairro": "Jardim das Flores",
            "cidade": "São Paulo",
            "estado": "SP",
            "numero": "123",
            "complemento": "Apto 101",
        },
        "doacoes": [
            {
                "fk_estoque_agape_id": itens[0].id,
                "quantidade": 9999,
            },
        ],
        "abrangencia": "cep",
    }

    response = test_client.put(
        f"/agape/editar-ciclo-acao-agape/{instancia_acao_agape.id}",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": f"Quantidade insuficiente em estoque do item {itens[0].item}."
    }
