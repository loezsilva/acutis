import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

CARD_RENDA_FAMILIAR_ENDPOINT = (
    '/api/agape/card-renda-familiar-agape/{familia_id}'
)


def test_card_renda_familiar_agape_sucesso_com_renda(
    client: FlaskClient, membro_token, seed_familia_com_membros_e_rendas
):
    """
    Testa o card de renda familiar para uma família com membros e rendas.
    """
    familia, renda_total_esperada, numero_membros_esperado = (
        seed_familia_com_membros_e_rendas
    )

    response = client.get(
        CARD_RENDA_FAMILIAR_ENDPOINT.format(familia_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert int(response.status_code) == HTTPStatus.OK
    response_data = response.json

    assert 'renda_familiar' in response_data
    assert 'renda_per_capta' in response_data


def test_card_renda_familiar_agape_familia_nao_encontrada(
    client: FlaskClient, membro_token
):
    """
    Testa o card de renda familiar para um ID de família inexistente.
    """
    id_familia_inexistente = uuid.uuid4()

    response = client.get(
        CARD_RENDA_FAMILIAR_ENDPOINT.format(familia_id=id_familia_inexistente),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
