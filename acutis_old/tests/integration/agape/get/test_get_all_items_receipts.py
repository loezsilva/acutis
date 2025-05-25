from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_all_items_receipts_success(
    test_client: FlaskClient, seed_admin_user_token, seed_stock_statistics
):
    instancia_acao_agape, _, doacao_agape = seed_stock_statistics

    response = test_client.get(
        f"/agape/listar-itens-recebidos/{instancia_acao_agape.id}/{doacao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["itens_recebidos"]) > 0
    assert "item" in response.json["itens_recebidos"][0]
    assert "quantidade" in response.json["itens_recebidos"][0]


def test_get_all_items_receipts_error_action_instance_not_found(
    test_client: FlaskClient, seed_admin_user_token
):
    response = test_client.get(
        "/agape/listar-itens-recebidos/9999/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ciclo de ação ágape nao encontrado."}
