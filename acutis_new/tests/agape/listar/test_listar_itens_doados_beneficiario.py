import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

BASE_ENDPOINT = 'api/agape/listar-itens-doados-beneficiario'


def test_listar_itens_doados_sucesso(
    client: FlaskClient,
    seed_doacao_com_itens_doados,
    membro_token,
):
    """
    Testa a listagem bem-sucedida de itens doados para um beneficiário
    quando a doação possui itens.
    """
    doacao_id, itens_esperados = seed_doacao_com_itens_doados

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(doacao_id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    resultados = resposta_json['resultados']

    assert isinstance(resultados, list), 'A resposta deveria ser uma lista.'
    assert len(resultados) == len(itens_esperados), (
        f'Esperado {len(itens_esperados)} itens doados, '
        f'recebido {len(resultados)}.'
    )

    itens_retornados_formatados = sorted(
        [
            {
                'nome_item': item['nome_item'],
                'quantidade': item['quantidade'],
            }
            for item in resultados
        ],
        key=lambda x: x['nome_item'],
    )

    itens_esperados_formatados = sorted(
        [
            {
                'nome_item': item['nome_item'],
                'quantidade': item['quantidade_doada'],
            }
            for item in itens_esperados
        ],
        key=lambda x: x['nome_item'],
    )

    assert itens_retornados_formatados == itens_esperados_formatados, (
        'A lista de itens doados retornada não corresponde à esperada.'
    )


def test_listar_itens_doados_para_doacao_sem_itens(
    client: FlaskClient,
    seed_doacao_sem_itens,  # Fixture para este cenário
    membro_token,
):
    """
    Testa a listagem de itens doados para uma doação que não possui itens.
    Espera-se uma resposta HTTPStatus.OK com uma lista vazia.
    """
    doacao_id = seed_doacao_sem_itens

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(doacao_id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    resultados = resposta_json['resultados']

    assert isinstance(resultados, list), 'A resposta deveria ser uma lista.'
    assert len(resultados) == 0, (
        'A lista de doações deveria estar vazia para uma doação sem itens.'
    )


def test_listar_itens_doados_doacao_inexistente(
    client: FlaskClient,
    membro_token,
):
    """
    Testa a listagem de itens doados para um doacao_id inexistente.
    Espera-se uma resposta HTTPStatus.NOT_FOUND.
    """
    id_doacao_inexistente = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(id_doacao_inexistente)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_itens_doados_nao_autorizado(
    client: FlaskClient,
):
    """
    Testa a tentativa de listar itens doados sem autenticação.
    Espera-se uma resposta HTTPStatus.UNAUTHORIZED.
    """
    id_doacao_qualquer = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(id_doacao_qualquer)}',
        # Nenhum header de Authorization é enviado
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
    # Opcional: Verificar corpo da resposta para mensagem de erro específica
