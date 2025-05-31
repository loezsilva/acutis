import uuid
from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.benfeitores.listar import (
    ListarDoacoesAnonimasBenfeitorUseCase,
)


def test_listar_doacoes_anonimas_benfeitor_sucesso(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    total_registros = 1

    campanha = seed_campanha_doacao
    _, doacao = seed_dados_doacao(
        campanha=campanha, doacao_recorrente=False, anonimo=True
    )

    response = client.get(
        f'/api/admin/benfeitores/listar-doacoes-anonimas-benfeitor/{
            str(doacao.fk_benfeitor_id)
        }',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['doacoes'][0]['data'] == (
        datetime.today().date().strftime('%d/%m/%Y')
    )
    assert response.json['doacoes'][0]['hora'] is not None
    assert response.json['doacoes'][0]['valor'] == 10.0


@patch.object(ListarDoacoesAnonimasBenfeitorUseCase, 'execute')
def test_listar_doacoes_anonimas_benfeitor_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        f'/api/admin/benfeitores/listar-doacoes-anonimas-benfeitor/{
            str(uuid.uuid4())
        }',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
