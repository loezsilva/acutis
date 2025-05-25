from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_agape_family_by_cpf_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
):
    instancia_acao_agape, _, membro_agape, _, _ = (
        seed_get_beneficiaries_and_items
    )

    response = test_client.get(
        f"/agape/buscar-familia-agape-por-cpf/{membro_agape.cpf}/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["familia"] is not None
    assert response.json["endereco"] is not None
    assert response.json["fotos_familia"] is not None
    assert len(response.json["fotos_familia"]) == 3


def test_get_agape_family_by_cpf_error_family_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_get_beneficiaries_and_items,
):
    instancia_acao_agape, _, _, _, _ = seed_get_beneficiaries_and_items
    cpf = "114.914.470-01"

    response = test_client.get(
        f"/agape/buscar-familia-agape-por-cpf/{cpf}/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {
        "error": "Família não encontrada pelo CPF informado."
    }
