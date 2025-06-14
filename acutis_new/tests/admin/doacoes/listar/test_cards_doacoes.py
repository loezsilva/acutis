from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from flask.testing import FlaskClient

from acutis_api.application.use_cases.admin.doacoes.listar import (
    RecorrenciaNaoEfetuadaUseCase,
    RecorrenciasCanceladasUseCase,
    RecorrenciasEfetuadasUseCase,
    RecorrenciasLembretesEfetivosUseCase,
    RecorrenciasPrevistasUseCase,
    RecorrenciaTotalUseCase,
)
from acutis_api.communication.enums.admin_doacoes import (
    StatusProcessamentoEnum,
)
from acutis_api.infrastructure.extensions import database
from tests.factories import LembreteDoacaoRecorrenteFactory


def test_card_doacoes_do_dia_not_found(client: FlaskClient, membro_token):
    response = client.get(
        '/api/admin/doacoes/card-total-do-dia',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Nenhuma doação efetuada.'}]


def test_card_doacoes_do_dia(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes,
    seed_campanha_doacao,
):
    _, _ = seed_gera_4_doacoes(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.get(
        '/api/admin/doacoes/card-total-do-dia',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'porcentagem': -25.0,
        'total': 10,
        'quantidade': 1,
    }


def test_card_doacoes_do_mes_atual_not_found(
    client: FlaskClient, membro_token
):
    response = client.get(
        '/api/admin/doacoes/card-total-do-mes',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Nenhuma doação efetuada.'}]


def test_card_doacoes_do_mes_atual(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
):
    _, _ = seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.get(
        '/api/admin/doacoes/card-total-do-mes',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'porcentagem': -25.0,
        'total': 10,
        'quantidade': 1,
    }


def test_card_media_diaria_not_found(client: FlaskClient, membro_token):
    response = client.get(
        '/api/admin/doacoes/card-media-diaria',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Nenhuma doação efetuada.'}]


def test_card_media_diaria(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes,
    seed_campanha_doacao,
):
    _, _ = seed_gera_4_doacoes(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.get(
        '/api/admin/doacoes/card-media-diaria',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'media': 13.33}


def test_card_media_mensal_not_found(client: FlaskClient, membro_token):
    response = client.get(
        '/api/admin/doacoes/card-media-mensal',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Nenhuma doação efetuada.'}]


def test_card_media_mensal(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
):
    _, _ = seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.get(
        '/api/admin/doacoes/card-media-mensal',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'media': 13.33}


def test_card_recorrencias_nao_efetuadas(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
):
    data_criacao = datetime.now() - relativedelta(months=1)
    seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao,
        criado_em=data_criacao,
        status_doacao=StatusProcessamentoEnum.expirado,
    )

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-nao-efetuadas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.json['total'] == 40
    assert response.status_code == HTTPStatus.OK
    assert response.json['qtd_doacoes'] == 4


@patch.object(RecorrenciaNaoEfetuadaUseCase, 'execute')
def test_card_recorrencias_nao_efetuadas_erro_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-nao-efetuadas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]


def test_card_recorrencias_total(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_gera_4_doacoes,
    seed_campanha_doacao,
):
    data_criacao = datetime.now() - relativedelta(months=1)
    seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao,
        criado_em=data_criacao,
        status_doacao=StatusProcessamentoEnum.pago,
    )

    seed_gera_4_doacoes(
        campanha=seed_campanha_doacao,
        status_doacao=StatusProcessamentoEnum.expirado,
    )

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-total',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.json['total'] == 80
    assert response.status_code == HTTPStatus.OK
    assert response.json['qtd_doacoes'] == 8
    assert response.json['qtd_doadores'] == 2


@patch.object(RecorrenciaTotalUseCase, 'execute')
def test_card_recorrencias_total_erro_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-total',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]


def test_card_recorrentes_previstas(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
):
    data_criacao = (
        datetime.now() - relativedelta(months=1) + relativedelta(days=1)
    )

    seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao,
        criado_em=data_criacao,
        status_doacao=StatusProcessamentoEnum.pendente,
    )

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-previstas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.json['total'] == 40
    assert response.status_code == HTTPStatus.OK
    assert response.json['qtd_doacoes'] == 4


@patch.object(RecorrenciasPrevistasUseCase, 'execute')
def test_card_recorrentes_previstas_erro_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-previstas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]


def test_card_lembretes_efetivos(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
    seed_registrar_membro,
):
    _, membro, _ = seed_registrar_membro()

    _, doacoes = seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao,
        status_doacao=StatusProcessamentoEnum.pago,
    )

    processamentos = doacoes.pagamento_doacao.processamentos_doacoes

    lembrete = LembreteDoacaoRecorrenteFactory(
        fk_processamento_doacao_id=processamentos[0].id,
        criado_por=membro.id,
    )
    database.session.add(lembrete)
    database.session.commit()

    response = client.get(
        '/api/admin/doacoes/card-lembretes-efetivos',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == 10
    assert response.json['qtd_doacoes'] == 1
    assert response.json['qtd_doadores'] == 1


@patch.object(RecorrenciasLembretesEfetivosUseCase, 'execute')
def test_card_lembretes_efetivos_erro_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/doacoes/card-lembretes-efetivos',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]


def test_card_recorrentes_efetuadas(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
):
    seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao,
        status_doacao=StatusProcessamentoEnum.pago,
        criado_em=datetime.now(),
    )

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-efetuadas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == 40
    assert response.json['qtd_doacoes'] == 4


@patch.object(RecorrenciasEfetuadasUseCase, 'execute')
def test_card_recorrentes_efetuadas_erro_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-efetuadas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]


def test_card_recorrentes_canceladas(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
):
    data_criacao = datetime.now() - relativedelta(months=1)
    seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao,
        criado_em=data_criacao,
        doacao_ativa=False,
    )

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-canceladas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == 40
    assert response.json['qtd_doacoes'] == 4


@patch.object(RecorrenciasCanceladasUseCase, 'execute')
def test_card_recorrentes_canceladas_erro_servidor(
    mock_target, client: FlaskClient, membro_token
):
    mock_target.side_effect = Exception('Erro interno no servidor')

    response = client.get(
        '/api/admin/doacoes/card-recorrentes-canceladas',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json == [{'msg': 'Erro interno no servidor.'}]
