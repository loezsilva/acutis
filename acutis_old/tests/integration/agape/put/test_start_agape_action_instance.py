from http import HTTPStatus
from flask.testing import FlaskClient


def test_start_agape_action_instance_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_instance_not_started,
):
    instancia_acao_agape = seed_agape_action_instance_not_started

    response = test_client.put(
        f"/agape/iniciar-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"msg": "Ciclo da ação iniciado com sucesso."}


def test_start_agape_action_instance_error_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
):
    response = test_client.put(
        "/agape/iniciar-ciclo-acao-agape/7777",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ciclo da ação não encontrado."}


def test_start_agape_action_instance_error_already_started(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_instance_started,
):
    instancia_acao_agape = seed_agape_action_instance_started

    response = test_client.put(
        f"/agape/iniciar-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": "Ciclo da ação já iniciado ou finalizado."
    }


def test_start_agape_action_instance_error_other_instance_already_started(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_with_instance_already_started,
):
    instancia_acao_agape = seed_agape_action_with_instance_already_started

    response = test_client.put(
        f"/agape/iniciar-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": "Essa ação ágape já possui um ciclo em andamento."
    }
