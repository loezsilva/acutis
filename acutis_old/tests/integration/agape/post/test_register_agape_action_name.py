from http import HTTPStatus
from flask.testing import FlaskClient

from builder import db
from models.agape.acao_agape import AcaoAgape
from tests.factories import AcaoAgapeFactory


def test_register_agape_action_name_success(
    test_client: FlaskClient, seed_admin_user_token
):
    payload = {"nome": "Ação Ágape Teste"}

    response = test_client.post(
        "/agape/cadastrar-nome-acao-agape",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"msg": "Ação ágape cadastrada com sucesso."}

    agape_action: AcaoAgape = AcaoAgape.query.filter_by(
        nome=payload["nome"]
    ).first()
    assert agape_action is not None
    assert agape_action.created_at is not None


def test_register_agape_action_name_error_conflict(
    test_client: FlaskClient, seed_admin_user_token
):
    acao_agape = AcaoAgapeFactory(nome="Salvação da Nação")
    db.session.add(acao_agape)
    db.session.commit()

    payload = {"nome": "salvacao da nacao"}

    response = test_client.post(
        "/agape/cadastrar-nome-acao-agape",
        json=payload,
        headers=seed_admin_user_token,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json == {
        "error": f"Ação {payload['nome']} já cadastrada no sistema."
    }
