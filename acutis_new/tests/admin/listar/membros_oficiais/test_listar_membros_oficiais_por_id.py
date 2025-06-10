import uuid
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.membros_oficiais.listar import (
    ListarMembroOficialPorIdUseCase,
)


def test_listar_membro_oficial_por_id(
    client: FlaskClient,
    seed_membro_oficial_campos_adicionais,
    membro_token,
):
    membro_oficial = seed_membro_oficial_campos_adicionais

    response = client.get(
        f'/api/admin/membros-oficiais/listar-por-id/{str(membro_oficial.id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['id'] == str(membro_oficial.id)


def test_listar_membro_oficial_por_id_nao_encontrado(
    client: FlaskClient,
    membro_token,
):
    membro_oficial_id = '4f3f8a0d-b82a-4b35-88e3-fc8a9cfe0fd0'

    response = client.get(
        f'/api/admin/membros-oficiais/listar-por-id/{membro_oficial_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Membro oficial não encontrado.'}]


@patch.object(ListarMembroOficialPorIdUseCase, 'execute')
def test_listar_membro_oficial_por_id_erro_interno(
    mock_target,
    client: FlaskClient,
    membro_token,
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        f'/api/admin/membros-oficiais/listar-por-id/{str(uuid.uuid4())}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.get_json() == [{'msg': 'Erro interno no servidor.'}]
