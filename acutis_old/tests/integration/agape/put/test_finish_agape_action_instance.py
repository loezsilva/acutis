from http import HTTPStatus
from flask.testing import FlaskClient
from builder import db
from models.agape.instancia_acao_agape import StatusAcaoAgapeEnum


def test_finish_agape_action_instance_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_instance_ending,
) -> None:
    instancia_acao_agape, item_instancia_agape, estoque_agape = (
        seed_agape_action_instance_ending
    )
    quantidade_itens = 50

    response = test_client.put(
        f"/agape/finalizar-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {"msg": "Ciclo da ação finalizado com sucesso."}

    db.session.refresh(instancia_acao_agape)
    db.session.refresh(item_instancia_agape)
    db.session.refresh(estoque_agape)

    assert instancia_acao_agape.status == StatusAcaoAgapeEnum.finalizado
    assert instancia_acao_agape.data_termino is not None

    assert item_instancia_agape.quantidade == 0
    assert estoque_agape.quantidade == quantidade_itens


def test_finish_agape_action_instance_error_instance_not_found(
    test_client: FlaskClient,
    seed_admin_user_token,
) -> None:
    response = test_client.put(
        "/agape/finalizar-ciclo-acao-agape/9999",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "Ciclo da ação não encontrado."}


def test_finish_agape_action_instance_error_not_started(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_agape_action_instance_not_started,
) -> None:
    instancia_acao_agape = seed_agape_action_instance_not_started
    response = test_client.put(
        f"/agape/finalizar-ciclo-acao-agape/{instancia_acao_agape.id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json == {
        "error": "Ciclo da ação ainda não foi iniciado ou já foi finalizado."
    }
