from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_agape_instance_items_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
):
    instancia_acao_agape, _, _, _, _ = seed_get_beneficiaries_and_items

    response = test_client.get(
        f"/agape/buscar-itens-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["itens_ciclo_agape"]) > 0
