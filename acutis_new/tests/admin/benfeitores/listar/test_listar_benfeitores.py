from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.benfeitores.listar import (
    ListarBenfeitoresUseCase,
)


def test_listar_benfeitores_sucesso(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    total_registros = 1

    campanha = seed_campanha_doacao
    _, _ = seed_dados_doacao(
        campanha=campanha, doacao_recorrente=False, anonimo=True
    )

    response = client.get(
        '/api/admin/benfeitores/listar-benfeitores',  # NOSONAR
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['benfeitores'][0]['nome'] == 'Yan da Pororoca'
    assert response.json['benfeitores'][0]['montante_total'] == 10.0


def test_listar_benfeitores_filtros_sucesso(
    client: FlaskClient, membro_token, seed_campanha_doacao, seed_dados_doacao
):
    total_registros = 1

    campanha = seed_campanha_doacao
    _, doacao = seed_dados_doacao(
        campanha=campanha, doacao_recorrente=False, anonimo=True
    )

    response = client.get(
        f"""/api/admin/benfeitores/listar-benfeitores?tipo_ordenacao=asc&\
        &id={doacao.fk_benfeitor_id}&nome_documento=Yan&\
        &registrado_em_inicio={datetime.today().date()}&\
        &ultima_doacao_inicio={datetime.today().date()}&\
        &campanha_id={campanha.id}&somente_membros=true""",
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    assert response.json['benfeitores'][0]['nome'] == 'Yan da Pororoca'
    assert response.json['benfeitores'][0]['montante_total'] == 10.0


@patch.object(ListarBenfeitoresUseCase, 'execute')
def test_listar_benfeitores_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/benfeitores/listar-benfeitores',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
