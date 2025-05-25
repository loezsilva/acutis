from http import HTTPStatus
from flask.testing import FlaskClient


def test_register_agape_action_success(
    test_client: FlaskClient, seed_admin_user_token, seed_register_agape_action
):
    acao_agape, itens_estoque = seed_register_agape_action

    payload = {
        "fk_acao_agape_id": acao_agape.id,
        "endereco": {
            "cep": "83010-510",
            "rua": "Rua das Flores",
            "bairro": "Centro",
            "cidade": "São José dos Pinhais",
            "estado": "PR",
            "numero": "123",
        },
        "doacoes": [
            {"fk_estoque_agape_id": itens_estoque[0].id, "quantidade": 10},
            {"fk_estoque_agape_id": itens_estoque[1].id, "quantidade": 20},
        ],
        "abrangencia": "sem_restricao",
    }

    response = test_client.post(
        "/agape/cadastrar-acao-agape",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"msg": "Ação ágape cadastrada com sucesso."}


def test_register_agape_action_error_insufficient_stock(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_register_agape_action_insufficient_stock,
):
    acao_agape, item_estoque = seed_register_agape_action_insufficient_stock

    payload = {
        "fk_acao_agape_id": acao_agape.id,
        "endereco": {
            "cep": "83010-510",
            "rua": "Rua das Flores",
            "bairro": "Centro",
            "cidade": "São José dos Pinhais",
            "estado": "PR",
            "numero": "123",
        },
        "doacoes": [
            {"fk_estoque_agape_id": item_estoque[0].id, "quantidade": 10},
        ],
        "abrangencia": "sem_restricao",
    }

    response = test_client.post(
        "/agape/cadastrar-acao-agape",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": f"Quantidade insuficiente em estoque do item {item_estoque[0].item}."
    }
