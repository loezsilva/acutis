import uuid
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.campanha.listar import (
    ListarCadastrosCampanhaUseCase,
)
from acutis_api.communication.responses.campanha import (
    ListarCadastrosCampanhaSchema,
)


def test_listar_cadastros_campanha_sucesso(
    client: FlaskClient, membro_token, seed_registra_5_membros_campanha
):
    total_registros = 5

    _, campanha = seed_registra_5_membros_campanha

    response = client.get(
        f'/api/admin/campanhas/listar-cadastros-campanha/{campanha.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    for cadastros in response.json['cadastros']:
        assert ListarCadastrosCampanhaSchema.model_validate(cadastros)


@patch.object(ListarCadastrosCampanhaUseCase, 'execute')
def test_listar_cadastros_campanha_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        f'/api/admin/campanhas/listar-cadastros-campanha/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
