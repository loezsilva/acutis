from http import HTTPStatus
from flask.testing import FlaskClient
from builder import db
from models.agape.instancia_acao_agape import InstanciaAcaoAgape


def test_delete_agape_action_instance_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_instance_with_items,
) -> None:
    estoques, instancia_acao_agape = seed_agape_action_instance_with_items
    fk_instancia_acao_agape_id = instancia_acao_agape.id

    response = test_client.delete(
        f"/agape/deletar-ciclo-acao-agape/{fk_instancia_acao_agape_id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert all(estoque.quantidade == 20 for estoque in estoques)
    assert (
        db.session.get(InstanciaAcaoAgape, fk_instancia_acao_agape_id) is None
    )


def test_delete_agape_action_instance_error_instance_not_found(
    test_client: FlaskClient, seed_admin_user_token
) -> None:
    response = test_client.delete(
        "/agape/deletar-ciclo-acao-agape/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ciclo da ação não encontrado."}


def test_delete_agape_action_instance_error_instance_already_started(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_instance_already_started,
) -> None:
    instancia_acao_agape = seed_agape_action_instance_already_started

    response = test_client.delete(
        f"/agape/deletar-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": "Somentes ciclos não iniciados podem ser deletados."
    }
