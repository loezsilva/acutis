from http import HTTPStatus

from flask.testing import FlaskClient

# Define o endpoint da API
CARDS_ESTATISTICAS_FAMILIAS_ENDPOINT = (
    '/api/agape/cards-estatisticas-familias-agape'
)


def test_cards_estatisticas_familias_com_dados(
    client: FlaskClient, membro_token, seed_varias_familias_para_estatisticas
):
    """
    Testa as estatísticas de famílias ágape quando há dados no sistema.
    """
    expected_stats = seed_varias_familias_para_estatisticas

    response = client.get(
        CARDS_ESTATISTICAS_FAMILIAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    assert 'familias_cadastradas' in response_data
    assert int(response_data['familias_cadastradas'].split(' ')[0]) == int(
        expected_stats['total_familias']
    )


def test_cards_estatisticas_familias_sem_dados(
    client: FlaskClient, membro_token
):
    """
    Testa as estatísticas de famílias ágape quando não há famílias.
    """
    response = client.get(
        CARDS_ESTATISTICAS_FAMILIAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    response_data = response.json

    assert 'familias_cadastradas' in response_data
    assert int(response_data['familias_cadastradas'].split(' ')[0]) == 0
