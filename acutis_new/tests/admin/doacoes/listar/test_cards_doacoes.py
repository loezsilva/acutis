from http import HTTPStatus

from flask.testing import FlaskClient


def test_card_doacoes_do_dia_not_found(client: FlaskClient, membro_token):
    response = client.get(
        '/api/admin/doacoes/card-total-do-dia',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Nenhuma doação efetuada.'}]


def test_card_doacoes_do_dia(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes,
    seed_campanha_doacao,
):
    _, _ = seed_gera_4_doacoes(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.get(
        '/api/admin/doacoes/card-total-do-dia',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'porcentagem': -25.0,
        'total': 10,
        'quantidade': 1,
    }


def test_card_doacoes_do_mes_atual_not_found(
    client: FlaskClient, membro_token
):
    response = client.get(
        '/api/admin/doacoes/card-total-do-mes',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Nenhuma doação efetuada.'}]


def test_card_doacoes_do_mes_atual(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
):
    _, _ = seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.get(
        '/api/admin/doacoes/card-total-do-mes',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {
        'porcentagem': -25.0,
        'total': 10,
        'quantidade': 1,
    }


def test_card_media_diaria_not_found(client: FlaskClient, membro_token):
    response = client.get(
        '/api/admin/doacoes/card-media-diaria',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Nenhuma doação efetuada.'}]


def test_card_media_diaria(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes,
    seed_campanha_doacao,
):
    _, _ = seed_gera_4_doacoes(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.get(
        '/api/admin/doacoes/card-media-diaria',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'media': 13.33}


def test_card_media_mensal_not_found(client: FlaskClient, membro_token):
    response = client.get(
        '/api/admin/doacoes/card-media-mensal',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.get_json() == [{'msg': 'Nenhuma doação efetuada.'}]


def test_card_media_mensal(
    client: FlaskClient,
    membro_token,
    seed_gera_4_doacoes_mensais,
    seed_campanha_doacao,
):
    _, _ = seed_gera_4_doacoes_mensais(
        campanha=seed_campanha_doacao, doacao_ativa=True
    )

    response = client.get(
        '/api/admin/doacoes/card-media-mensal',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.get_json() == {'media': 13.33}
