import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

DELETAR_MEMBRO_ENDPOINT = 'api/agape/deletar-membro'


def test_deletar_membro_agape_sucesso(
    client: FlaskClient, membro_token, seed_membro_agape
):
    """Testa a exclusão bem-sucedida de uma família ágape."""
    membro_agape = seed_membro_agape

    resposta = client.delete(
        f'{DELETAR_MEMBRO_ENDPOINT}/{membro_agape.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NO_CONTENT


def test_deletar_membro_agape_nao_encontrado(
    client: FlaskClient, membro_token
):
    membro_invalido_id = uuid.uuid4()  # ID de família que não existe

    resposta = client.delete(
        f'{DELETAR_MEMBRO_ENDPOINT}/{membro_invalido_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_deletar_membro_agape_sem_permissao(client: FlaskClient):
    """
    Testa a tentativa de exclusão de uma família ágape sem permissão adequada.
    """
    membro_invalido_id = uuid.uuid4()

    resposta = client.delete(
        f'{DELETAR_MEMBRO_ENDPOINT}/{membro_invalido_id}',
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
