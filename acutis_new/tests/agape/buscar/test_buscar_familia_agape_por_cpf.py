from http import HTTPStatus

from flask.testing import FlaskClient

BUSCAR_FAMILIA_ENDPOINT = (
    '/api/agape/buscar-familia-agape-por-cpf/{cpf}/{ciclo_acao_id}'
)


def test_buscar_familia_agape_por_cpf_sucesso(
    client: FlaskClient,
    membro_token,
    seed_familia_com_cpf_especifico,
    seed_ciclo_acao_agape,
):
    """Testa a busca de família por CPF com sucesso."""
    familia = seed_familia_com_cpf_especifico
    ciclo_acao = seed_ciclo_acao_agape[0]

    cpf_membro_familia = '12345678901'

    response = client.get(
        BUSCAR_FAMILIA_ENDPOINT.format(
            cpf=cpf_membro_familia,
            ciclo_acao_id=ciclo_acao.id,
        ),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_json = response.json

    assert response_json['familia']['id'] == str(familia.id)
    assert 'endereco' in response_json
    assert 'fotos_familia_urls' in response_json


def test_buscar_familia_agape_por_cpf_nao_encontrado(
    client: FlaskClient, membro_token, seed_ciclo_acao_agape
):
    """Testa a busca de família por CPF quando a família não é encontrada."""
    cpf_inexistente = '12345678900'
    ciclo_acao = seed_ciclo_acao_agape[0]

    response = client.get(
        BUSCAR_FAMILIA_ENDPOINT.format(
            cpf=cpf_inexistente, ciclo_acao_id=ciclo_acao.id
        ),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_buscar_familia_agape_por_cpf_invalido(
    client: FlaskClient, membro_token, seed_ciclo_acao_agape
):
    """Testa a busca de família por CPF com um CPF inválido."""
    cpf_invalido = '123'
    ciclo_acao = seed_ciclo_acao_agape[0]

    response = client.get(
        BUSCAR_FAMILIA_ENDPOINT.format(
            cpf=cpf_invalido, ciclo_acao_id=ciclo_acao.id
        ),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
