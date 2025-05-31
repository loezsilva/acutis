import uuid
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.campanha.listar import (
    ListarDoacoesCampanhaUseCase,
)


def test_listar_doacoes_campanha_sucesso(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    total_registros = 1

    campanha = seed_campanha_doacao
    _, _ = seed_dados_doacao(campanha=campanha)

    response = client.get(
        f'/api/admin/campanhas/listar-doacoes-campanha/{campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['doacoes'][0]['forma_pagamento'] == 'credito'
    assert response.json['doacoes'][0]['nome'] == 'Yan da Pororoca'
    assert response.json['doacoes'][0]['valor'] == 10.0
    assert response.json['doacoes'][0]['data_doacao'] is not None


@patch.object(ListarDoacoesCampanhaUseCase, 'execute')
def test_listar_doacoes_campanha_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        f'/api/admin/campanhas/listar-doacoes-campanha/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
