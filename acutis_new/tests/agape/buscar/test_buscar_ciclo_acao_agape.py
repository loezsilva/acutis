# -*- coding: utf-8 -*-
import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

BUSCAR_ULTIMO_CICLO_ENDPOINT = (
    '/api/agape/buscar-ciclo-acao-agape/{ciclo_acao_id}'
)


def test_buscar_ciclo_acao_agape_sucesso(
    client: FlaskClient, membro_token, seed_ciclo_acao_com_itens
):
    """
    Testa a busca bem-sucedida do último ciclo de uma ação ágape.
    """
    ciclo_acao = seed_ciclo_acao_com_itens[0]
    response = client.get(
        BUSCAR_ULTIMO_CICLO_ENDPOINT.format(ciclo_acao_id=ciclo_acao.id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    response_data = response.json
    print('@', response_data['endereco'])
    assert response.status_code == HTTPStatus.OK
    assert 'id' in response_data
    assert str(ciclo_acao.id) == response_data['id']
    assert 'nome_acao_id' in response_data
    assert 'abrangencia' in response_data
    assert 'doacoes' in response_data
    assert 'endereco' in response_data


def test_buscar_ultimo_ciclo_acao_agape_nome_acao_nao_encontrado(
    client: FlaskClient, membro_token
):
    """
    Testa a busca do último ciclo para um ciclo_acao_id inexistente.
    """
    id_inexistente = uuid.uuid4()

    response = client.get(
        BUSCAR_ULTIMO_CICLO_ENDPOINT.format(ciclo_acao_id=id_inexistente),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_buscar_ultimo_ciclo_acao_agape_nome_acao_sem_token(
    client: FlaskClient,
):
    """
    Testa a busca do último ciclo para um ciclo_acao_id inexistente.
    """
    id_inexistente = uuid.uuid4()

    response = client.get(
        BUSCAR_ULTIMO_CICLO_ENDPOINT.format(ciclo_acao_id=id_inexistente),
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
