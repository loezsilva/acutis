import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

BASE_ENDPOINT = 'api/agape/listar-doacoes-recebidas'


def test_listar_doacoes_recebidas_familia_sucesso(
    client: FlaskClient,
    seed_familia_com_recebimentos,
    membro_token,
):
    """
    Testa a listagem bem-sucedida de doações recebidas por uma família.
    """
    familia = seed_familia_com_recebimentos[0]

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(familia.id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    resultados = resposta_json['resultados']

    assert isinstance(resultados, list), 'A resposta deveria ser uma lista.'

    for doacao in resultados:
        assert 'doacao_id' in doacao
        assert 'ciclo_acao_id' in doacao
        assert 'dia_horario' in doacao
        assert 'nome_acao' in doacao
        assert 'recibos' in doacao


def test_listar_doacoes_recebidas_familia_inexistente(
    client: FlaskClient,
    membro_token,
):
    id_familia_inexistente = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(id_familia_inexistente)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_doacoes_recebidas_familia_sem_doacoes(
    client: FlaskClient,
    seed_familia_com_endereco,
    membro_token,
):
    familia = seed_familia_com_endereco[0]

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(familia.id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    resultados = resposta_json['resultados']

    assert isinstance(resultados, list), 'A resposta deveria ser uma lista.'
    assert len(resultados) == 0, (
        'A lista de doações deveria estar vazia para uma família sem doações.'
    )


def test_listar_doacoes_recebidas_familia_nao_autorizado(
    client: FlaskClient,
):
    id_familia_qualquer = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(id_familia_qualquer)}',
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
