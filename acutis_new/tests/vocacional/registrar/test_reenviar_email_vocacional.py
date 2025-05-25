from http import HTTPStatus

from flask.testing import FlaskClient


def test_reenvia_email_vocacional(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_pendentes,
):
    pre_cadastro, _ = seed_pre_cadastro_vocacional_pendentes[0]

    response = client.post(
        '/api/vocacional/reenviar-email-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'usuario_vocacional_id': pre_cadastro.id},
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.OK


def test_reenvia_email_vocacional_reprovado(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_reprovado,
):
    pre_cadastro, _ = seed_pre_cadastro_vocacional_reprovado

    response = client.post(
        '/api/vocacional/reenviar-email-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'usuario_vocacional_id': str(pre_cadastro.id)},
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.CONFLICT
    data_response = response.get_json()

    assert data_response == [
        {
            'msg': 'Não foi possível enviar o email \
                pois o processo foi marcado como reprovado ou desistente.'
        }
    ]


def test_reenvia_email_vocacional_desistencia(
    client: FlaskClient,
    membro_token,
    seed_pre_cadastro_vocacional_desistencia,
):
    pre_cadastro, _ = seed_pre_cadastro_vocacional_desistencia()

    response = client.post(
        '/api/vocacional/reenviar-email-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'usuario_vocacional_id': pre_cadastro.id},
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.CONFLICT
    data_response = response.get_json()

    assert data_response == [
        {
            'msg': 'Não foi possível enviar o email \
                pois o processo foi marcado como reprovado ou desistente.'
        }
    ]


def test_reenvia_email_vocacional_nao_encontrado(
    client: FlaskClient,
    membro_token,
):
    response = client.post(
        '/api/vocacional/reenviar-email-vocacional',
        headers={'Authorization': f'Bearer {membro_token}'},
        json={'usuario_vocacional_id': '0C8C99E4-62A7-4D55-A793-0E6244E3ECB2'},
        content_type='application/json',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    data_response = response.get_json()

    assert data_response == [{'msg': 'Vocacional não encontrado.'}]
