from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_all_donations_receipts_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
):
    _, _, _, familia, _ = seed_get_beneficiaries_and_items
    response = test_client.get(
        f"/agape/listar-doacoes-recebidas/{familia.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json["doacoes_recebidas"]) > 0
    doacoes_recebidas = response.json["doacoes_recebidas"][0]
    assert doacoes_recebidas["dia_horario"] is not None
    assert doacoes_recebidas["nome_acao"] is not None
    assert len(doacoes_recebidas["recibos"]) > 0


def test_get_all_donations_receipts_error_family_not_found(
    test_client: FlaskClient, seed_admin_user_token
):

    response = test_client.get(
        "/agape/listar-doacoes-recebidas/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Familia não encontrada."}


def test_get_all_donations_receipts_error_family_deleted(
    test_client: FlaskClient, seed_admin_user_token, seed_family_deleted
):
    familia = seed_family_deleted
    response = test_client.get(
        f"/agape/listar-doacoes-recebidas/{familia.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Familia não encontrada."}
