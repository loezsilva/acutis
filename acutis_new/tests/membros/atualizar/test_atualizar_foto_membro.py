from http import HTTPStatus
from io import BytesIO

from flask.testing import FlaskClient

ROTA_ATUALIZAR_FOTO_MEMBRO = '/api/membros/atualizar-foto-membro'


def test_atualizar_foto_membro_sucesso(
    client: FlaskClient, seed_registrar_membro, membro_token
):
    lead, membro, endereco = seed_registrar_membro()

    foto_atualizada = {
        'fk_lead_id': str(membro.fk_lead_id),
        'foto': (BytesIO(b'fake_image_data'), 'foto_teste1.png'),
    }

    response = client.put(
        ROTA_ATUALIZAR_FOTO_MEMBRO,
        data=foto_atualizada,
        content_type='multipart/form-data',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['msg'] == 'Foto atualizada com sucesso.'


def test_atualizar_foto_membro_nenhuma_foto_adicionada(
    client: FlaskClient, seed_registrar_membro, membro_token
):
    lead, membro, endereco = seed_registrar_membro()

    foto_vazia = {'fk_lead_id': str(membro.fk_lead_id)}

    response = client.put(
        ROTA_ATUALIZAR_FOTO_MEMBRO,
        data=foto_vazia,
        content_type='multipart/form-data',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json[0]['msg'] == 'Nenhuma foto nova adicionada.'
