from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.benfeitores.buscar import (
    BuscarCardsBenfeitoresUseCase,
)


def test_buscar_cards_benfeitores_sucesso(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    campanha = seed_campanha_doacao
    _, _ = seed_dados_doacao(
        campanha=campanha, doacao_recorrente=False, anonimo=True
    )

    response = client.get(
        '/api/admin/benfeitores/buscar-cards-benfeitores',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'benfeitores': {'percentual': 0.0, 'total': 1},
        'doacoes_anonimas': {'percentual': 0.0, 'total': 1},
        'montante': {'percentual': 0.0, 'total': 10.0},
        'ticket_medio': {'percentual': 0.0, 'total': 10.0},
    }


@patch.object(BuscarCardsBenfeitoresUseCase, 'execute')
def test_buscar_cards_benfeitores_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/benfeitores/buscar-cards-benfeitores',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
