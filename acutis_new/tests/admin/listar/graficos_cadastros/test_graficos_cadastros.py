from datetime import datetime
from http import HTTPStatus

from flask.testing import FlaskClient
from sqlalchemy import func

from acutis_api.domain.entities.lead import Lead
from acutis_api.infrastructure.extensions import database


def test_grafico_leads_do_mes(
    client: FlaskClient, seed_registra_13_leads, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/quantidade-leads-mes-atual',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    assert 'porcentagem' in response.get_json()
    assert 'quantidade_leads_mes_atual' in response.get_json()


def test_grafico_leads_media_mensal(
    client: FlaskClient, seed_registra_13_leads, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/leads-media-mensal',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'leads_media_mensal' in response.get_json()


def test_grafico_leads_do_mes_nao_autorizado(
    client: FlaskClient, seed_registra_13_leads, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/quantidade-leads-mes-atual'
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_grafico_membros_do_mes(
    client: FlaskClient, seed_registra_10_membros, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/quantidade-cadastros-mes-atual',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'porcentagem' in response.get_json()
    assert 'quantidade_cadastro_mes_atual' in response.get_json()


def test_grafico_membros_media_mensal(
    client: FlaskClient, seed_registra_10_membros, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/membros-media-mensal',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'membros_media_mensal' in response.get_json()


def test_grafico_membros_do_dia(
    client: FlaskClient, seed_registra_10_membros, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/quantidade-cadastros-dia-atual',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'porcentagem' in response.get_json()
    assert 'quantidade_cadastro_dia_atual' in response.get_json()


def test_grafico_membros_media_diaria(
    client: FlaskClient, seed_registra_10_membros, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/membros-media-diaria',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'membros_media_diaria' in response.get_json()


def test_grafico_resumo_quantidade_cadastros(
    client: FlaskClient,
    seed_10_benfeitores,
    membro_token,
):
    response = client.get(
        '/api/admin/graficos-cadastros/resumo-quantidade-registros',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'leads' in response.get_json()
    assert 'membros' in response.get_json()
    assert 'benfeitores' in response.get_json()

    assert response.get_json()['leads'] == 11  # noqa
    assert response.get_json()['membros'] == 11  # noqa
    assert response.get_json()['benfeitores'] == 10  # noqa


def test_membros_por_genero(
    client: FlaskClient, seed_registra_10_membros, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/membros-por-genero',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert 'feminino' in response.get_json()
    assert 'masculino' in response.get_json()
    assert 'outros' in response.get_json()


def test_grafico_leads_por_hora(
    client: FlaskClient, seed_registra_13_leads, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/quantidade-leads-por-hora',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK


def test_grafico_membros_por_hora_dia_atual(
    client: FlaskClient, seed_registra_10_membros, membro_token
):
    response_por_hora_dia_atual = client.get(
        '/api/admin/graficos-cadastros/membros-por-hora-dia-atual',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response_por_hora_dia_atual.status_code == HTTPStatus.OK

    resposta = response_por_hora_dia_atual.get_json()

    valida_resposta = []
    tempo_atual = datetime.now().hour
    for hora in range(0, tempo_atual + 1):
        valida_resposta.append({
            'hora': f'{hora:02d}:00',
            'quantidade': resposta[hora]['quantidade'] or 0,
        })

    assert resposta == valida_resposta

    assert resposta[-1]['hora'] == f'{tempo_atual:02d}:00'
    assert resposta[-1]['quantidade'] == 9  # noqa

    response_total_dia_atual = client.get(
        '/api/admin/graficos-cadastros/quantidade-cadastros-dia-atual',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response_total_dia_atual.status_code == HTTPStatus.OK
    total_membros_dia_atual = response_total_dia_atual.get_json()[
        'quantidade_cadastro_dia_atual'
    ]

    quantidade_total = 0
    for i in resposta:
        quantidade_total += i['quantidade']

    assert quantidade_total == total_membros_dia_atual


def test_grafico_membros_por_dia_mes_atual(
    client: FlaskClient, seed_registra_10_membros, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/membros-por-dia-mes-atual',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    resposta = response.get_json()
    resposta[-1]['quantidade'] = 9  # noqa


def test_grafico_leads_por_origem(
    client: FlaskClient, seed_leads_por_origem, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/leads-por-origem',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    resposta = response.get_json()

    for i in resposta:
        if i['origem'] == 'acutis':
            assert i['quantidade'] == 5  # noqa
            assert i['porcentagem'] == 38.46  # NOSONAR # noqa
        if i['origem'] == 'google':
            assert i['quantidade'] == 4  # noqa
            assert i['porcentagem'] == 30.77  # NOSONAR # noqa
        if i['origem'] == 'app':
            assert i['quantidade'] == 4  # noqa
            assert i['porcentagem'] == 30.77  # NOSONAR # noqa


def test_grafico_leads_por_dia_da_semana(
    client: FlaskClient, seed_leads_por_origem, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/leads-por-dia-da-semana',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    dias_semana = {
        0: 'segunda',
        1: 'terça',
        2: 'quarta',
        3: 'quinta',
        4: 'sexta',
        5: 'sabado',
        6: 'domingo',
    }
    dia_semana = datetime.now().weekday()

    assert response.status_code == HTTPStatus.OK

    data = response.get_json()
    for i in data:
        if i['dia_semana'] == dias_semana[dia_semana]:
            assert i['quantidade'] == 13  # noqa
        else:
            assert i['quantidade'] == 0  # noqa


def test_grafico_leads_por_campanha_mes_atual(
    client: FlaskClient, seed_15_leads_campanhas, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/leads-por-campanha-mes-atual',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    quantidade_campanha_general = 0  # noqa
    quantidade_campanha_peixe = 0  # noqa
    quantidade_campanha_agua = 0  # noqa

    for i in response.get_json():
        if i['campanha'] == 'Campanha do General':
            quantidade_campanha_general += i['quantidade']

        if i['campanha'] == 'Campanha do Peixe':
            quantidade_campanha_peixe += i['quantidade']

        if i['campanha'] == 'Campanha da Água':
            quantidade_campanha_agua += i['quantidade']

    assert quantidade_campanha_general == 5  # noqa
    assert quantidade_campanha_peixe == 5  # noqa
    assert quantidade_campanha_agua == 5  # noqa


def test_grafico_leads_cada_mes(
    client: FlaskClient, seed_15_leads_campanhas, membro_token
):
    response = client.get(
        '/api/admin/graficos-cadastros/cadastros-por-mes',
        headers={'Authorization': f' Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    quantidade_mes_atual = client.get(
        '/api/admin/graficos-cadastros/quantidade-leads-mes-atual',
        headers={'Authorization': f' Bearer {membro_token}'},
    )
    assert quantidade_mes_atual.status_code == HTTPStatus.OK

    assert (
        response.get_json()[-1]['quantidade']
        == (quantidade_mes_atual.get_json()['quantidade_leads_mes_atual'])
    )


def test_grafico_membros_por_idade(
    client: FlaskClient, membro_token, seed_registra_15_membros_idade
):
    response = client.get(
        '/api/admin/graficos-cadastros/cadastros-por-idade',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    for item in response.get_json():
        if item['faixa_etaria'] == '15-24':
            assert item['feminino'] == 0
            assert item['masculino'] == 6  # noqa
        if item['faixa_etaria'] == '35-44':
            assert item['feminino'] == 5  # noqa
            assert item['masculino'] == 0
        if item['faixa_etaria'] == '45-59':
            assert item['feminino'] == 0
            assert item['masculino'] == 5  # noqa


def test_grafico_leads_evolucao_mensal(
    client: FlaskClient,
    membro_token,
    seed_registra_10_membros,
    seed_registra_15_membros_idade,
):
    response = client.get(
        '/api/admin/graficos-cadastros/leads-por-evolucao-mensal',
        headers={'Authorization': f' Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    total_leads = database.session.query(func.count(Lead.id)).scalar()

    assert response.get_json()[-1]['montante_acumulado'] == total_leads
