import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_finalizar_ciclo_acao_sucesso(
    client: FlaskClient, seed_ciclo_acao_com_itens, membro_token
):
    ciclo_acao = seed_ciclo_acao_com_itens[0]

    def _request():
        response = client.put(
            f'/api/agape/finalizar-ciclo-acao-agape/{ciclo_acao.id}',
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        return response

    response = _request()

    assert response.status_code == HTTPStatus.OK
    assert (
        response.json['msg'].lower() == 'ciclo da ação finalizado com sucesso.'
    )

    response = _request()
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        response.json[0]['msg'].lower()
        == 'ciclo da ação ainda não foi iniciado ou já foi finalizado.'
    )


def test_erro_finalizar_ciclo_ja_finalizado(
    client: FlaskClient, membro_token, seed_ciclo_acao_agape_finalizado
):
    response = client.put(
        f'/api/agape/finalizar-ciclo-acao-agape/{seed_ciclo_acao_agape_finalizado.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        response.json[0]['msg'].lower()
        == 'ciclo da ação ainda não foi iniciado ou já foi finalizado.'
    )


def test_erro_finalizar_ciclo_acao_inexistente(
    client: FlaskClient, membro_token
):
    response = client.put(
        f'/api/agape/finalizar-ciclo-acao-agape/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json[0]['msg'].lower() == 'ciclo da ação não encontrado.'


def test_erro_finalizar_ciclo_acao_sem_token(client: FlaskClient):
    response = client.put(
        f'/api/agape/finalizar-ciclo-acao-agape/{str(uuid.uuid4())}',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
