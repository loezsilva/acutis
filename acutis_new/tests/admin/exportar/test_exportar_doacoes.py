from http import HTTPStatus

from flask.testing import FlaskClient


def preparar_url():
    colunas = [
        'valor_doacao',
        'recorrente',
        'forma_pagamento',
        'codigo_ordem_pagamento',
        'anonimo',
        'gateway',
        'ativo',
        'processado_em',
        'codigo_referencia',
        'codigo_transacao',
        'codigo_comprovante',
        'nosso_numero',
        'status_processamento',
    ]

    url = '/api/admin/exportar/doacoes?'
    for coluna in colunas:
        url += f'colunas={coluna}&'
    return url


def test_exportar_doacoes_sucesso(
    client: FlaskClient, seed_campanha_doacao, seed_dados_doacao, membro_token
):
    campanha = seed_campanha_doacao
    seed_dados_doacao(campanha=campanha)

    url = preparar_url()

    response = client.get(
        url,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['url'] is not None
    assert response.json['msg'] == 'Exportados 1 registros'
