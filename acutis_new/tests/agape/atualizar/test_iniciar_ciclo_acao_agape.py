import uuid
from http import HTTPStatus

from flask.testing import FlaskClient


def test_iniciar_ciclo_acao_sucesso_e_erro_ciclo_ja_iniciado(
    client: FlaskClient, seed_ciclo_acao_agape, membro_token
):
    ciclo_acao = seed_ciclo_acao_agape[0]

    def _request():
        response = client.put(
            f'/api/agape/iniciar-ciclo-acao-agape/{ciclo_acao.id}',
            headers={'Authorization': f'Bearer {membro_token}'},
        )

        return response

    response = _request()

    assert response.status_code == HTTPStatus.OK
    assert (
        response.json['msg'].lower() == 'ciclo da ação iniciado com sucesso.'
    )

    response = _request()
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json[0]['msg'].lower()
        == 'ciclo da ação já iniciado ou finalizado.'
    )


def test_erro_iniciar_ciclo_acao_inexistente(
    client: FlaskClient, membro_token
):
    response = client.put(
        f'/api/agape/iniciar-ciclo-acao-agape/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json[0]['msg'].lower() == 'ciclo da ação não encontrado.'
