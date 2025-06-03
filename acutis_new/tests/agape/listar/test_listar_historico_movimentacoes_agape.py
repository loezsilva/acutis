from http import HTTPStatus

from flask.testing import FlaskClient

LISTAR_HISTORICO_MOVIMENTACOES_ENDPOINT = (
    'api/agape/listar-historico-movimentacoes'
)


def test_listar_historico_movimentacoes_sucesso_com_dados(
    client: FlaskClient,
    seed_historico_movimentacoes_agape,
    membro_token,
):
    dados_semeados = seed_historico_movimentacoes_agape
    total_itens_semeados = len(dados_semeados)

    resposta_pagina = client.get(
        LISTAR_HISTORICO_MOVIMENTACOES_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta_pagina.status_code == HTTPStatus.OK
    dados_resposta = resposta_pagina.json

    assert 'resultados' in dados_resposta
    assert 'pagina' in dados_resposta
    assert 'paginas' in dados_resposta
    assert len(dados_resposta['resultados']) == total_itens_semeados


def test_listar_historico_movimentacoes_nao_autorizado(
    client: FlaskClient,
):
    """
    Testa a tentativa de listar o histórico de movimentações sem autenticação.
    Espera-se uma resposta HTTPStatus.UNAUTHORIZED.
    """
    resposta = client.get(
        LISTAR_HISTORICO_MOVIMENTACOES_ENDPOINT,
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
