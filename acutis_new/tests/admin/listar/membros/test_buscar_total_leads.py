from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.membros import (
    BuscarTotalLeadsUseCase,
)


def test_buscar_total_leads_sucesso(
    client: FlaskClient,
    seed_registra_13_leads,
    membro_token,
):
    response = client.get(
        '/api/admin/membros/buscar-total-leads',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {'total_leads': 13}


@patch.object(BuscarTotalLeadsUseCase, 'execute')
def test_buscar_total_leads_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/membros/buscar-total-leads',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
