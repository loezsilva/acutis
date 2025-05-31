from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.campanha.listar import (
    CadastrosCampanhaPorPeriodoUseCase,
)
from acutis_api.communication.responses.campanha import (
    CadastrosCampanhaPorPeriodoResponse,
)

ROTA = '/api/admin/campanhas/cadastros-campanha-por-periodo'


def test_listar_cadastros_campanha_por_periodo_sucesso(
    client: FlaskClient,
    seed_gerar_cadastros_campanha_em_periodos,
    membro_token
):
    campanha_id = seed_gerar_cadastros_campanha_em_periodos

    response = client.get(
        f'{ROTA}/{campanha_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json
    assert CadastrosCampanhaPorPeriodoResponse.model_validate(data)
    assert data['ultimas_24h'] == 2
    assert data['ultimos_7_dias'] == 4
    assert data['ultimo_mes'] == 6


@patch.object(CadastrosCampanhaPorPeriodoUseCase, 'execute')
def test_buscar_membros_mes_erro_interno_servidor(
    mock_target,
    client: FlaskClient,
    seed_gerar_cadastros_campanha_em_periodos,
    membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    campanha_id = seed_gerar_cadastros_campanha_em_periodos

    response = client.get(
        f'{ROTA}/{campanha_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
