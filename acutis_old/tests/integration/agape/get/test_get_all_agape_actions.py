from http import HTTPStatus
from flask.testing import FlaskClient

from models.schemas.agape.get.get_all_agape_actions import (
    AgapeActionSchema,
    GetAllAgapeActionsResponse,
)


def test_get_all_agape_actions_success(
    test_client: FlaskClient, seed_admin_user_token, seed_get_all_agape_actions
):
    response = test_client.get(
        "/agape/listar-acoes-agape", headers=seed_admin_user_token
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json["total"] > 0
    assert len(response.json["acoes_agape"]) > 0


def test_get_all_agape_actions_fk_acao_agape_id_filter(
    test_client: FlaskClient, seed_admin_user_token, seed_get_all_agape_actions
):
    acoes_agape = [
        (sorted(seed_get_all_agape_actions, key=lambda acao: acao.nome))[0]
    ]

    ciclos_finalizados = 3
    total = 1

    schema = [
        AgapeActionSchema(
            id=acao.id,
            nome=acao.nome,
            data_cadastro=acao.created_at.strftime("%Y-%m-%d %H:%M:%S.%f"),
            ciclos_finalizados=ciclos_finalizados,
        ).dict()
        for acao in acoes_agape
    ]

    expected = GetAllAgapeActionsResponse(
        page=1, total=total, acoes_agape=schema
    ).dict()

    response = test_client.get(
        f"/agape/listar-acoes-agape?fk_acao_agape_id={acoes_agape[0].id}",
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == expected
