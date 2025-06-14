import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

BASE_ENDPOINT = 'api/agape/listar-geolocalizacoes-beneficiarios-ciclo-acao'


def test_listar_geolocalizacoes_sucesso_com_dados(
    client: FlaskClient,
    seed_geolocalizacoes_beneficiarios_ciclo_acao,
    membro_token,
):
    """
    Testa a listagem bem-sucedida de geolocalizações de beneficiários
    de um ciclo de ação específico quando existem dados.
    """
    ciclo_acao_id, geolocalizacoes_esperadas = (
        seed_geolocalizacoes_beneficiarios_ciclo_acao
    )

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(ciclo_acao_id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    resultados = resposta_json['resultados']

    assert 'ciclo_acao_id' in resposta_json
    assert 'nome_familia' in resultados[0]
    assert 'latitude' in resultados[0]
    assert 'longitude' in resultados[0]
    assert isinstance(resultados, list), 'A resposta deveria ser uma lista.'
    assert len(resultados) == len(geolocalizacoes_esperadas), (
        f'Esperado {len(geolocalizacoes_esperadas)} geolocalizações, '
        f'recebido {len(resultados)}.'
    )


def test_listar_geolocalizacoes_ciclo_inexistente(
    client: FlaskClient,
    membro_token,
):
    """
    Testa a listagem de geolocalizações para um ciclo_acao_id inexistente.
    Espera-se uma resposta HTTPStatus.NOT_FOUND.
    """
    id_ciclo_inexistente = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(id_ciclo_inexistente)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_geolocalizacoes_nao_autorizado(
    client: FlaskClient,
):
    ciclo_acao_id_qualquer = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(ciclo_acao_id_qualquer)}',
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
