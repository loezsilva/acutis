from datetime import datetime, timedelta
from http import HTTPStatus

from flask.testing import FlaskClient

from acutis_api.application.utils.funcoes_auxiliares import buscar_data_valida
from acutis_api.communication.enums.campanhas import (
    ObjetivosCampanhaEnum,
    PeriodicidadePainelCampanhasEnum,
)

ROTA = '/api/admin/campanhas/painel-campanhas'


def test_painel_campanhas_doacao_diario(
    client: FlaskClient, seed_campanha_doacao, membro_token, seed_dados_doacao
):
    campanha_doacao = seed_campanha_doacao

    seed_dados_doacao(campanha=campanha_doacao)
    payload = {
        'lista_painel': [
            {
                'campanha_id': str(campanha_doacao.id),
                'periodicidade': PeriodicidadePainelCampanhasEnum.diario,
            }
        ]
    }

    response = client.post(
        ROTA,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.json['campanhas'][0].get('total') == 10
    assert response.status_code == HTTPStatus.OK


def test_painel_campanhas_doacao_semanal(
    client: FlaskClient,
    seed_campanha_doacao,
    membro_token,
    seed_dados_doacao,
):
    campanha_doacao = seed_campanha_doacao

    seed_dados_doacao(
        campanha=campanha_doacao,
        criado_em=datetime.now(),
        numero_documento='10144088388',
    )
    seed_dados_doacao(
        campanha=campanha_doacao,
        criado_em=datetime.now(),
        numero_documento='10122088388',
    )
    seed_dados_doacao(
        campanha=campanha_doacao, criado_em=datetime.now() - timedelta(days=7)
    )

    payload = {
        'lista_painel': [
            {
                'campanha_id': str(campanha_doacao.id),
                'periodicidade': PeriodicidadePainelCampanhasEnum.semanal,
            }
        ]
    }

    response = client.post(
        ROTA,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.json['campanhas'][0].get('total') == 20
    assert response.json['campanhas'][0].get('porcentagem_crescimento') == 100
    assert response.status_code == HTTPStatus.OK


def test_painel_campanhas_doacao_mensal(
    client: FlaskClient,
    seed_campanha_doacao,
    membro_token,
    seed_dados_doacao,
):
    campanha_doacao = seed_campanha_doacao

    hoje = datetime.now()
    dia = hoje.day
    mes = hoje.month
    ano = hoje.year

    if mes == 1:
        mes_anterior = 12
        ano_anterior = ano - 1
    else:
        mes_anterior = mes - 1
        ano_anterior = ano

    data_mes_passado = datetime.combine(
        buscar_data_valida(dia, mes_anterior, ano_anterior),
        datetime.min.time(),
    )

    seed_dados_doacao(
        campanha=campanha_doacao,
        criado_em=datetime.now(),
        numero_documento='10144088388',
    )
    seed_dados_doacao(
        campanha=campanha_doacao,
        criado_em=data_mes_passado,
        numero_documento='10122088388',
    )
    seed_dados_doacao(campanha=campanha_doacao, criado_em=data_mes_passado)

    payload = {
        'lista_painel': [
            {
                'campanha_id': str(campanha_doacao.id),
                'periodicidade': PeriodicidadePainelCampanhasEnum.mensal,
            }
        ]
    }

    response = client.post(
        ROTA,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.json['campanhas'][0].get('total') == 10
    assert response.json['campanhas'][0].get('porcentagem_crescimento') == -50
    assert response.status_code == HTTPStatus.OK


def test_painel_campanhas_cadastro(
    client: FlaskClient,
    seed_campanha_objetivo_dinamico,
    seed_vincula_na_campanha_verifica_periodo,
    membro_token,
):
    campanha_cadastro = seed_campanha_objetivo_dinamico(
        ObjetivosCampanhaEnum.cadastro
    )

    seed_vincula_na_campanha_verifica_periodo(
        campanha_cadastro, PeriodicidadePainelCampanhasEnum.diario
    )

    payload = {
        'lista_painel': [
            {
                'campanha_id': str(campanha_cadastro.id),
                'periodicidade': PeriodicidadePainelCampanhasEnum.diario,
            }
        ]
    }

    response = client.post(
        ROTA,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['campanhas'][0].get('total') == 4
    assert response.json['campanhas'][0].get('porcentagem_crescimento') == 300


def test_painel_campanhas_pre_cadastro_semanal(
    client: FlaskClient,
    seed_campanha_objetivo_dinamico,
    seed_vincula_na_campanha_verifica_periodo,
    membro_token,
):
    campanha_pre_cadastro = seed_campanha_objetivo_dinamico(
        ObjetivosCampanhaEnum.pre_cadastro
    )

    seed_vincula_na_campanha_verifica_periodo(
        campanha_pre_cadastro, PeriodicidadePainelCampanhasEnum.semanal
    )

    payload = {
        'lista_painel': [
            {
                'campanha_id': str(campanha_pre_cadastro.id),
                'periodicidade': PeriodicidadePainelCampanhasEnum.semanal,
            }
        ]
    }

    response = client.post(
        ROTA,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['campanhas'][0].get('total') == 4
    assert response.json['campanhas'][0].get('porcentagem_crescimento') == 300


def test_painel_campanhas_oficial_mensal(
    client: FlaskClient,
    seed_campanha_objetivo_dinamico,
    seed_vincula_na_campanha_verifica_periodo,
    membro_token,
):
    campanha_oficial = seed_campanha_objetivo_dinamico(
        ObjetivosCampanhaEnum.oficiais
    )

    seed_vincula_na_campanha_verifica_periodo(
        campanha_oficial, PeriodicidadePainelCampanhasEnum.mensal
    )

    payload = {
        'lista_painel': [
            {
                'campanha_id': str(campanha_oficial.id),
                'periodicidade': PeriodicidadePainelCampanhasEnum.mensal,
            }
        ]
    }

    response = client.post(
        ROTA,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['campanhas'][0].get('total') == 4
    assert response.json['campanhas'][0].get('porcentagem_crescimento') == 300


def test_painel_campanhas_campanha_nao_encontrada(
    client: FlaskClient,
    membro_token,
):
    payload = {
        'lista_painel': [
            {
                'campanha_id': '3f4e0d7e-8ad5-45ae-8e18-1e1c29fc0299',
                'periodicidade': PeriodicidadePainelCampanhasEnum.diario,
            }
        ]
    }

    response = client.post(
        ROTA,
        json=payload,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == [
        {
            'msg': 'Campanha com ID 3f4e0d7e-8ad5-45ae-8e18-1e1c29fc0299 '
            'não encontrada.'
        }
    ]
