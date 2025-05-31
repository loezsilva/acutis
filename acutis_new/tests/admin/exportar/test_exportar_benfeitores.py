from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.exportar_dados.benfeitores import (
    ExportarBenfeitoresUseCase,
)


def preparar_url():
    colunas = [
        'benfeitor_id',
        'nome',
        'registrado_em',
        'numero_documento',
        'nome_campanha',
        'quantidade_doacoes',
        'montante',
        'ultima_doacao',
    ]

    url = '/api/admin/exportar/benfeitores?'
    for coluna in colunas:
        url += f'colunas={coluna}&'
    return url


def test_exportar_benfeitores_sucesso(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    campanha = seed_campanha_doacao
    _, _ = seed_dados_doacao(
        campanha=campanha, doacao_recorrente=False, anonimo=True
    )

    url = preparar_url()

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['url'] is not None
    assert response.json['msg'] == 'Exportados 1 registros'


def test_exportar_benfeitores_filtros_sucesso(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    campanha = seed_campanha_doacao
    _, _ = seed_dados_doacao(
        campanha=campanha, doacao_recorrente=False, anonimo=True
    )

    url = preparar_url()

    url += f'nome_documento=Yan&\
        &registrado_em_inicio={datetime.today().date()}&\
        &ultima_doacao_inicio={datetime.today().date()}&\
        &campanha_id={campanha.id}&campanha_nome={campanha.nome}'

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['url'] is not None
    assert response.json['msg'] == 'Exportados 1 registros'


@patch.object(ExportarBenfeitoresUseCase, 'execute')
def test_exportar_benfeitores_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    url = preparar_url()

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
