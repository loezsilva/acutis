from http import HTTPStatus

from flask.testing import FlaskClient

ENDPOINT = '/api/agape/listar-nomes-acoes'


def test_listar_nomes_acoes(
    client: FlaskClient, seed_nome_acao_agape, membro_token
):
    response = client.get(
        ENDPOINT, headers={'Authorization': f'Bearer {membro_token}'}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json

    # Validar estrutura de paginação na resposta
    assert 'resultados' in data

    resultado = data['resultados'][0]

    assert 'nome' in resultado

    assert resultado['id'] == str(seed_nome_acao_agape.id)
