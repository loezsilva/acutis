import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

CARD_TOTAL_RECEBIMENTOS_ENDPOINT = (
    '/api/agape/card-total-recebimentos/{familia_id}'
)


def test_card_total_recebimentos_sucesso_com_itens(
    client: FlaskClient, membro_token, seed_familia_com_recebimentos
):
    """
    Testa o card de total de recebimentos para uma família com doações e itens.
    """
    (
        familia,
        quantidade_total_itens_esperada,
    ) = seed_familia_com_recebimentos

    response = client.get(
        CARD_TOTAL_RECEBIMENTOS_ENDPOINT.format(familia_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    assert 'total_itens_recebidos' in response_data
    assert (
        f'{quantidade_total_itens_esperada} itens recebidos'.lower()
        in response_data['total_itens_recebidos'].lower()
    )


def test_card_total_recebimentos_familia_sem_recebimentos(
    client: FlaskClient, membro_token, seed_familia_com_endereco
):
    """
    Testa o card de total de recebimentos para uma família sem doações.
    """
    familia = seed_familia_com_endereco[0]

    response = client.get(
        CARD_TOTAL_RECEBIMENTOS_ENDPOINT.format(familia_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    assert 'total_itens_recebidos' in response_data
    assert (
        '0 itens recebidos'.lower()
        in response_data['total_itens_recebidos'].lower()
    )


def test_card_total_recebimentos_familia_nao_encontrada(
    client: FlaskClient, membro_token
):
    """
    Testa o card de total de recebimentos para um ID de família inexistente.
    """
    id_familia_inexistente = uuid.uuid4()

    response = client.get(
        CARD_TOTAL_RECEBIMENTOS_ENDPOINT.format(
            familia_id=id_familia_inexistente
        ),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
