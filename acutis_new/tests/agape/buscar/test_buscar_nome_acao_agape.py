# -*- coding: utf-8 -*-
import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

BUSCAR_NOME_ACAO_ENDPOINT = '/api/agape/buscar-nome-acao-agape/{nome_acao_id}'


def test_buscar_nome_acao_agape_sucesso(
    client: FlaskClient, membro_token, seed_ciclo_acao_agape
):
    """
    Testa a busca bem-sucedida do último ciclo de uma ação ágape.
    """
    ciclo_acao = seed_ciclo_acao_agape[0]
    nome_acao_id = ciclo_acao.fk_acao_agape_id
    response = client.get(
        BUSCAR_NOME_ACAO_ENDPOINT.format(nome_acao_id=nome_acao_id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    assert response_data['id'] == str(nome_acao_id)
    assert response_data['abrangencia'] == ciclo_acao.abrangencia

    assert 'endereco' in response_data
    assert 'doacoes' in response_data
    assert 'endereco' in response_data


def test_buscar_nome_acao_seed_nome_acao_agape_sem_acao(
    client: FlaskClient, membro_token, seed_nome_acao_agape
):
    """
    Testa a busca bem-sucedida do último ciclo de uma ação ágape.
    """
    nome_acao_id = seed_nome_acao_agape
    response = client.get(
        BUSCAR_NOME_ACAO_ENDPOINT.format(nome_acao_id=nome_acao_id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_buscar_nome_acao_agape_nome_acao_nao_encontrado(
    client: FlaskClient, membro_token
):
    """
    Testa a busca do último ciclo para um nome_acao_id inexistente.
    """
    id_inexistente = uuid.uuid4()

    response = client.get(
        BUSCAR_NOME_ACAO_ENDPOINT.format(nome_acao_id=id_inexistente),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_buscar_nome_acao_agape_nome_acao_sem_token(
    client: FlaskClient,
):
    """
    Testa a busca do último ciclo para um nome_acao_id inexistente.
    """
    id_inexistente = uuid.uuid4()

    response = client.get(
        BUSCAR_NOME_ACAO_ENDPOINT.format(nome_acao_id=id_inexistente),
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
