from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_agape_action_by_id_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
):
    _, acao_agape, _, _, _ = seed_get_beneficiaries_and_items
    qtd_doacoes = 2

    response = test_client.get(
        f"/agape/buscar-acao-agape/{acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["doacoes"]) == qtd_doacoes
    assert "endereco" in response.json
    assert "abrangencia" in response.json


def test_get_agape_action_by_id_error_last_instance_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
):
    acao_agape_inexistente = 9999

    response = test_client.get(
        f"/agape/buscar-acao-agape/{acao_agape_inexistente}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {
        "error": "Última instância da ação ágape não encontrada."
    }
