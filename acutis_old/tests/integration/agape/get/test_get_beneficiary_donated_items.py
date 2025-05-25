from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_beneficiary_donated_items_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
):
    _, _, _, _, doacao_agape = seed_get_beneficiaries_and_items

    response = test_client.get(
        f"/agape/listar-itens-doados-beneficiario/{doacao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["itens_doados"]) == 2
