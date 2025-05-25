import uuid
from http import HTTPStatus
from unittest.mock import patch

from flask.testing import FlaskClient

from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.infrastructure.services.maxipago import MaxiPago


@patch.object(MaxiPago, 'estornar_pagamento')
def test_estornar_doacao_recorrente_sucesso(  # NOSONAR
    mock_estornar_pagamento,
    client: FlaskClient,
    seed_dados_doacao,
    seed_campanha_doacao,
    membro_token,
):
    mock_estornar_pagamento.return_value

    campanha = seed_campanha_doacao
    _, doacao = seed_dados_doacao(campanha=campanha, doacao_ativa=True)

    processamento_doacao_id = doacao.pagamento_doacao.processamentos_doacoes[
        0
    ].id

    response = client.post(
        f'/api/doacoes/pagamento/cartao-de-credito/estornar/{processamento_doacao_id}',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'msg': 'O estorno do valor foi efetuado com sucesso.'
    }


@patch.object(MaxiPago, 'estornar_pagamento')
def test_estornar_doacao_unica_sucesso(  # NOSONAR
    mock_estornar_pagamento,
    client: FlaskClient,
    seed_dados_doacao,
    seed_campanha_doacao,
):
    mock_estornar_pagamento.return_value

    campanha = seed_campanha_doacao
    lead, doacao = seed_dados_doacao(
        campanha=campanha, doacao_ativa=True, doacao_recorrente=False
    )

    processamento_doacao_id = doacao.pagamento_doacao.processamentos_doacoes[
        0
    ].id

    payload = {'email': lead.email, 'senha': '@Teste;1234'}

    resp_token = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = resp_token.json['access_token']

    response = client.post(
        f'/api/doacoes/pagamento/cartao-de-credito/estornar/{processamento_doacao_id}',  # noqa
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        'msg': 'O estorno do valor foi efetuado com sucesso.'
    }


def test_estornar_doacao_erro_processamento_doacao_nao_encontrado(  # NOSONAR
    client: FlaskClient,
    membro_token,
):
    processamento_doacao_inexistente_id = str(uuid.uuid4())

    response = client.post(
        f'/api/doacoes/pagamento/cartao-de-credito/estornar/{processamento_doacao_inexistente_id}',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json[0] == {
        'msg': f'Ops, processamento da doação com id {processamento_doacao_inexistente_id} não encontrado.'  # noqa
    }


def test_estornar_doacao_erro_doacao_ja_estornada(  # NOSONAR
    client: FlaskClient,
    seed_dados_doacao,
    seed_campanha_doacao,
    membro_token,
):
    campanha = seed_campanha_doacao
    _, doacao = seed_dados_doacao(
        campanha=campanha,
        doacao_ativa=True,
        status_doacao=StatusProcessamentoEnum.estornado,
    )

    processamento_doacao_id = doacao.pagamento_doacao.processamentos_doacoes[
        0
    ].id

    response = client.post(
        f'/api/doacoes/pagamento/cartao-de-credito/estornar/{processamento_doacao_id}',  # noqa
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json[0] == {
        'msg': 'Ops, essa doação já consta como estornada.'
    }
