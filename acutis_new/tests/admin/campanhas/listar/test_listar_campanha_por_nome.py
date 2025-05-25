from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.communication.responses.campanha import (
    ListaCampanhaPorNomeResponse,
)

ROTA = '/api/admin/campanhas/buscar-campanha-por-nome'


def test_listar_campanha_por_nome(
    client: FlaskClient, seed_campanha_membros_oficiais, membro_token
):
    campanha = seed_campanha_membros_oficiais
    nome_campanha = campanha.nome

    response = client.get(
        f'{ROTA}/{nome_campanha}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert ListaCampanhaPorNomeResponse.model_validate(response.json)


def test_campanha_invalida(client: FlaskClient, membro_token):
    response = client.get(
        f'{ROTA}/naoexistente',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [{'msg': 'Campanha não encontrada'}]
