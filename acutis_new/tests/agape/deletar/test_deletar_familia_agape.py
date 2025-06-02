import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

DELETAR_FAMILIA_ENDPOINT = 'api/agape/deletar-familia'


def test_deletar_familia_agape_sucesso(
    client: FlaskClient, membro_token, seed_familia_com_endereco
):
    """Testa a exclusão bem-sucedida de uma família ágape."""
    familia = seed_familia_com_endereco[0]

    resposta = client.delete(
        f'{DELETAR_FAMILIA_ENDPOINT}/{familia.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NO_CONTENT


def test_deletar_familia_agape_nao_encontrada(
    client: FlaskClient, membro_token
):
    familia_invalida_id = uuid.uuid4()  # ID de família que não existe

    resposta = client.delete(
        f'{DELETAR_FAMILIA_ENDPOINT}/{familia_invalida_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_deletar_familia_agape_sem_permissao(client: FlaskClient):
    """
    Testa a tentativa de exclusão de uma família ágape sem permissão adequada.
    """
    familia_invalida_id = uuid.uuid4()

    resposta = client.delete(
        f'{DELETAR_FAMILIA_ENDPOINT}/{familia_invalida_id}',
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
