from http import HTTPStatus

from flask.testing import FlaskClient

ENDPOINT = '/api/agape/listar-ciclo-acoes-agape'


def test_listar_ciclo_acoes_agape(
    client: FlaskClient, seed_ciclo_acao_agape, membro_token
):
    ciclo_acao = seed_ciclo_acao_agape[0]
    response = client.get(
        ENDPOINT, headers={'Authorization': f'Bearer {membro_token}'}
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json

    # Validar estrutura de paginação na resposta
    assert 'resultados' in data
    assert 'pagina' in data
    assert 'total' in data
    assert 'paginas' in data

    assert data['total'] > 0

    resultado = data['resultados'][0]

    assert 'id' in resultado
    assert 'nome_acao_id' in resultado
    assert 'status' in resultado

    assert resultado['id'] == str(ciclo_acao.id)
