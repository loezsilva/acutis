import uuid
from http import HTTPStatus
from io import BytesIO

from flask.testing import FlaskClient

REGISTRAR_RECIBOS_BASE_ENDPOINT = '/api/agape/registrar-recibos-doacao-agape'


def test_registrar_recibos_sucesso(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_doacao_com_itens_doados,
):
    token = seed_lead_voluntario_e_token[1]
    doacao_id, _ = seed_doacao_com_itens_doados

    endpoint = f'{REGISTRAR_RECIBOS_BASE_ENDPOINT}/{doacao_id}'

    data = {
        'recibos': [
            (BytesIO(b'foto'), 'foto_teste.png'),
        ]
    }
    resposta = client.post(
        endpoint,
        headers={
            'Authorization': f'Bearer {token}',
        },
        content_type='multipart/form-data',
        data=data,
    )

    assert resposta.status_code == HTTPStatus.CREATED


def test_registrar_recibos_doacao_inexistente(
    client: FlaskClient, seed_lead_voluntario_e_token
):
    token = seed_lead_voluntario_e_token[1]
    random_doacao_id = uuid.uuid4()
    endpoint = f'{REGISTRAR_RECIBOS_BASE_ENDPOINT}/{random_doacao_id}'
    data = {
        'recibos': [
            (BytesIO(b'foto'), 'foto_teste.png'),
        ]
    }
    resposta = client.post(
        endpoint,
        headers={
            'Authorization': f'Bearer {token}',
        },
        content_type='multipart/form-data',
        data=data,
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_registrar_recibos_payload_invalido_recibo_vazio(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_doacao_com_itens_doados,
):
    token = seed_lead_voluntario_e_token[1]
    doacao_id, _ = seed_doacao_com_itens_doados
    endpoint = f'{REGISTRAR_RECIBOS_BASE_ENDPOINT}/{doacao_id}'
    data = {'recibos': []}
    resposta = client.post(
        endpoint,
        headers={
            'Authorization': f'Bearer {token}',
        },
        content_type='multipart/form-data',
        data=data,
    )
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_registrar_recibos_payload_invalido_sem_campo_recibo(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_doacao_com_itens_doados,
):
    token = seed_lead_voluntario_e_token[1]
    doacao_id, _ = seed_doacao_com_itens_doados
    endpoint = f'{REGISTRAR_RECIBOS_BASE_ENDPOINT}/{doacao_id}'
    payload = {}  # Payload sem o campo 'recibo'

    resposta = client.post(
        endpoint, headers={'Authorization': f'Bearer {token}'}, data=payload
    )
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_registrar_recibos_sem_permissao(
    client: FlaskClient, seed_doacao_com_itens_doados
):
    doacao_id, _ = seed_doacao_com_itens_doados
    endpoint = f'{REGISTRAR_RECIBOS_BASE_ENDPOINT}/{doacao_id}'
    data = {'recibos': []}
    resposta = client.post(
        endpoint, content_type='multipart/form-data', data=data
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
