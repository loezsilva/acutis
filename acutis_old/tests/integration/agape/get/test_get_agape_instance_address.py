from http import HTTPStatus
from flask.testing import FlaskClient


def test_get_agape_instance_address_success(
    test_client: FlaskClient, seed_admin_user_token, seed_agape_action
):
    instancia_acao_agape, endereco = seed_agape_action

    response = test_client.get(
        f"/agape/buscar-endereco-instancia-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "abrangencia": instancia_acao_agape.abrangencia,
        "bairro": endereco.bairro,
        "cep": endereco.cep,
        "cidade": endereco.cidade,
        "complemento": endereco.complemento,
        "estado": endereco.estado,
        "numero": endereco.numero,
        "rua": endereco.rua,
    }


def test_get_agape_instance_address_error_instance_not_found(
    test_client: FlaskClient, seed_admin_user_token
):

    response = test_client.get(
        "/agape/buscar-endereco-instancia-acao-agape/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ciclo de ação ágape não encontrado."}
