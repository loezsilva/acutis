from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient
from freezegun import freeze_time

from acutis_api.application.use_cases.admin.membros import (
    BuscarLeadsMesUseCase,
)


def test_buscar_leads_mes_sucesso(
    client: FlaskClient,
    membro_token,
    seed_registrar_membro,
):
    hoje = datetime.today()
    ano = hoje.year
    mes = hoje.month - 1

    if mes == 0:
        mes = 12
        ano -= 1

    dia = min(
        hoje.day,
        [
            31,
            29 if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0) else 28,
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ][mes - 1],
    )

    data_mes_passado = datetime(ano, mes, dia)

    seed_registrar_membro(criado_em=data_mes_passado)

    seed_registrar_membro()

    response = client.get(
        '/api/admin/membros/buscar-leads-mes',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['leads_mes'] == 2
    assert response.json['porcentagem_crescimento'] == 100


def test_buscar_leads_mes_janeiro(
    client: FlaskClient, membro_token, seed_registrar_membro
):
    with freeze_time('2025-01-01'):
        seed_registrar_membro(criado_em=datetime.now())

        response = client.get(
            '/api/admin/membros/buscar-leads-mes',
            headers={'Authorization': f'Bearer {membro_token}'},
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json['leads_mes'] == 1
        assert response.json['porcentagem_crescimento'] == 0


@patch.object(BuscarLeadsMesUseCase, 'execute')
def test_buscar_leads_mes_erro_interno_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/membros/buscar-leads-mes',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
