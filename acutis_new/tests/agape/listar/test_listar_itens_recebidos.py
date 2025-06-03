import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

BASE_ENDPOINT = 'api/agape/listar-itens-recebidos'


def test_listar_itens_recebidos_sucesso(
    client: FlaskClient,
    seed_itens_recebidos_em_ciclo_doacao,
    membro_token,
):
    """
    Testa a listagem bem-sucedida de itens recebidos para um ciclo e doação
    específicos, quando existem dados.
    """
    ciclo_id, doacao_id, itens_esperados = seed_itens_recebidos_em_ciclo_doacao

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(ciclo_id)}/{str(doacao_id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json

    assert isinstance(resposta_json, list), 'A resposta deveria ser uma lista.'
    assert len(resposta_json) == len(itens_esperados), (
        f'Esperado {len(itens_esperados)} itens recebidos, '
        f'recebido {len(resposta_json)}.'
    )

    itens_retornados_formatados = sorted(
        [
            {
                'item_id': str(item['item_id']),
                'nome_item': item['nome_item'],
                'quantidade_doada': item['quantidade_doada'],
                'item_doacao_agape_id': str(item['item_doacao_agape_id']),
                'item_instancia_agape_id': str(
                    item['item_instancia_agape_id']
                ),
            }
            for item in resposta_json
        ],
        key=lambda x: x['nome_item'],
    )

    itens_esperados_formatados = sorted(
        [
            {
                'item_id': str(item['item_id']),
                'nome_item': item['nome_item'],
                'quantidade_doada': item['quantidade_doada'],
                'item_doacao_agape_id': str(item['item_doacao_agape_id']),
                'item_instancia_agape_id': str(
                    item['item_instancia_agape_id']
                ),
            }
            for item in itens_esperados
        ],
        key=lambda x: x['nome_item'],
    )

    assert itens_retornados_formatados == itens_esperados_formatados, (
        'A lista de itens recebidos retornada não corresponde à esperada.'
    )


def test_listar_itens_recebidos_doacao_sem_itens(
    client: FlaskClient,
    seed_doacao_em_ciclo_sem_itens,
    membro_token,
):
    """
    Testa a listagem de itens para uma doação que existe em um ciclo,
    mas não possui itens registrados (ItemDoacaoAgape).
    Espera-se uma resposta HTTPStatus.OK com uma lista vazia.
    """
    ciclo_id, doacao_id = seed_doacao_em_ciclo_sem_itens

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(ciclo_id)}/{str(doacao_id)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json

    assert isinstance(resposta_json, list), 'A resposta deveria ser uma lista.'
    assert len(resposta_json) == 0, (
        'A lista de itens deveria estar vazia para uma doação sem itens '
        'registrados no ciclo.'
    )


def test_listar_itens_recebidos_doacao_pertence_a_outro_ciclo(
    client: FlaskClient,
    seed_itens_recebidos_em_ciclo_doacao,
    seed_ciclo_acao_agape,
    membro_token,
):
    """
    Testa a listagem de itens quando a doação existe, mas os itens
    dessa doação não pertencem ao ciclo_acao_id fornecido na URL.
    Espera-se uma lista vazia, pois a combinação ciclo/doação não tem itens.
    """
    _, doacao_id_principal, _ = seed_itens_recebidos_em_ciclo_doacao

    ciclo_secundario_id, _ = seed_ciclo_acao_agape

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(ciclo_secundario_id)}/{str(doacao_id_principal)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_itens_recebidos_ciclo_inexistente(
    client: FlaskClient,
    membro_token,
):
    """
    Testa a listagem quando o ciclo_acao_id é inexistente.
    Espera-se HTTPStatus.NOT_FOUND.
    """
    doacao_id_invalido = uuid.uuid4()
    ciclo_id_inexistente = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(ciclo_id_inexistente)}/{str(doacao_id_invalido)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_itens_recebidos_doacao_inexistente(
    client: FlaskClient,
    seed_itens_recebidos_em_ciclo_doacao,  # Para ter um ciclo_id válido
    membro_token,
):
    """
    Testa a listagem quando o doacao_id é inexistente.
    Espera-se HTTPStatus.NOT_FOUND.
    """
    ciclo_id_valido, _, _ = seed_itens_recebidos_em_ciclo_doacao
    doacao_id_inexistente = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(ciclo_id_valido)}/{str(doacao_id_inexistente)}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_itens_recebidos_nao_autorizado(
    client: FlaskClient,
):
    """
    Testa a tentativa de listar itens recebidos sem autenticação.
    Espera-se uma resposta HTTPStatus.UNAUTHORIZED.
    """
    ciclo_id_qualquer = uuid.uuid4()
    doacao_id_qualquer = uuid.uuid4()

    resposta = client.get(
        f'{BASE_ENDPOINT}/{str(ciclo_id_qualquer)}/{str(doacao_id_qualquer)}',
    )
    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
