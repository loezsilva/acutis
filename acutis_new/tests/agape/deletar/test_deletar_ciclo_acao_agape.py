import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_deletar_ciclo_acao_sucesso(
    client: FlaskClient, seed_ciclo_acao_agape, membro_token
):
    response = client.delete(
        f'/api/agape/deletar-ciclo-acao-agape/{seed_ciclo_acao_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_erro_deletar_ciclo_acao_em_andamento(
    client: FlaskClient, seed_ciclo_acao_agape_em_andamento, membro_token
):
    response = client.delete(
        f'/api/agape/deletar-ciclo-acao-agape/{
            seed_ciclo_acao_agape_em_andamento.id
        }',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg'].lower()
        == 'somentes ciclos não iniciados podem ser deletados.'
    )


def test_erro_deletar_ciclo_acao_inexistente(
    client: FlaskClient, membro_token
):
    response = client.delete(
        f'/api/agape/deletar-item/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert 'msg' in response.json[0]
