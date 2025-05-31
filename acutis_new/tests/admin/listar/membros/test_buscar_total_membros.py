from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.membros import (
    BuscarTotalMembrosUseCase,
)


def test_buscar_total_membros_sucesso(
    client: FlaskClient,
    membro_token,
):
    response = client.get(
        '/api/admin/membros/buscar-total-membros',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'total_membros': 1}


@patch.object(BuscarTotalMembrosUseCase, 'execute')
def test_buscar_total_membros_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/membros/buscar-total-membros',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
