import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

BUSCAR_MEMBRO_ENDPOINT = '/api/agape/buscar-membro/{membro_agape_id}'


def test_buscar_membro_agape_por_id_sucesso(
    client: FlaskClient, membro_token, seed_membro_agape
):
    """Testa a busca de um membro ágape pelo ID com sucesso."""
    membro_familia = seed_membro_agape

    response = client.get(
        BUSCAR_MEMBRO_ENDPOINT.format(membro_agape_id=membro_familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    assert response_data['id'] == str(membro_familia.id)
    assert response_data['nome'] == membro_familia.nome
    assert response_data['email'] == membro_familia.email
    assert response_data['cpf'] == membro_familia.cpf


def test_buscar_membro_agape_por_id_nao_encontrado(
    client: FlaskClient, membro_token
):
    """Testa a busca de um membro ágape com um ID inexistente."""
    id_inexistente = uuid.uuid4()

    response = client.get(
        BUSCAR_MEMBRO_ENDPOINT.format(membro_agape_id=id_inexistente),
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
