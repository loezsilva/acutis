from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.cargos_oficiais import (
    ObterTotalCadastrosCargoOficialUseCase,
)

TOTAL_CADASTROS_POR_CARGO_ENDPOINT = (
    '/api/admin/cargos-oficiais/cadastros-por-cargo'
)


def test_total_cadastros_por_cargo_oficial_sucesso(
    client: FlaskClient,
    seed_membros_oficial_general_status_dinamico,
    seed_membros_oficial_general_com_superior,
    seed_membros_oficial_marechal_status_dinamico,
    membro_token,
):
    seed_membros_oficial_general_status_dinamico(status='aprovado')

    response = client.get(
        TOTAL_CADASTROS_POR_CARGO_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.get_json()

    cargos = {
        item['nome_cargo'].lower(): item['total_cadastros_cargo']
        for item in data
    }

    assert 'general' in cargos
    assert 'marechal' in cargos

    assert cargos['general'] == 3
    assert cargos['marechal'] == 1


@patch.object(ObterTotalCadastrosCargoOficialUseCase, 'execute')
def test_obter_total_cadastros_cargo_oficial_erro_interno_servidor(
    mock_target,
    client: FlaskClient,
    membro_token,
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        TOTAL_CADASTROS_POR_CARGO_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
