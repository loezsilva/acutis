import uuid
from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.benfeitores.buscar import (
    BuscarInformacoesBenfeitorUseCase,
)


def test_buscar_informacoes_benfeitor_sucesso(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    campanha = seed_campanha_doacao
    _, doacao = seed_dados_doacao(
        campanha=campanha, doacao_recorrente=False, anonimo=True
    )

    response = client.get(
        f'/api/admin/benfeitores/buscar-informacoes-benfeitor/{
            str(doacao.fk_benfeitor_id)
        }',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'id': str(doacao.fk_benfeitor_id),
        'nome': 'Yan da Pororoca',
        'numero_documento': '14069725334',
        'registrado_em': datetime.today().date().strftime('%d/%m/%Y'),
        'total_doacoes': 1,
        'total_valor_doado': 10.0,
        'ultima_doacao': datetime.today().date().strftime('%d/%m/%Y'),
    }


@patch.object(BuscarInformacoesBenfeitorUseCase, 'execute')
def test_buscar_informacoes_benfeitor_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        f'/api/admin/benfeitores/buscar-informacoes-benfeitor/{
            str(uuid.uuid4())
        }',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
