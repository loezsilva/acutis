import uuid
from http import HTTPStatus

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

    recibo_data_str = f'https://example.com/recibo/{uuid.uuid4()}'

    payload = {'recibos': [{'recibo': recibo_data_str}]}

    resposta = client.post(
        endpoint, headers={'Authorization': f'Bearer {token}'}, json=payload
    )

    assert resposta.status_code == HTTPStatus.CREATED

    resposta_json = resposta.json

    assert 'recibos_criados' in resposta_json
    assert isinstance(resposta_json['recibos_criados'], list)
    assert len(resposta_json['recibos_criados']) == 1

    recibo_criado_resposta = resposta_json['recibos_criados'][0]
    assert 'id' in recibo_criado_resposta
    assert recibo_criado_resposta['fk_doacao_agape_id'] == str(doacao_id)
    assert recibo_criado_resposta['recibo'] == recibo_data_str
    assert 'criado_em' in recibo_criado_resposta


def test_registrar_recibos_doacao_inexistente(
    client: FlaskClient, seed_lead_voluntario_e_token
):
    token = seed_lead_voluntario_e_token[1]
    random_doacao_id = uuid.uuid4()
    endpoint = f'{REGISTRAR_RECIBOS_BASE_ENDPOINT}/{random_doacao_id}'
    payload = {'recibos': [{'recibo': 'https://example.com/recibo/test'}]}

    resposta = client.post(
        endpoint, headers={'Authorization': f'Bearer {token}'}, json=payload
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
    payload = {'recibos': []}  # Recibo vazio

    resposta = client.post(
        endpoint, headers={'Authorization': f'Bearer {token}'}, json=payload
    )
    assert resposta.status_code == HTTPStatus.BAD_REQUEST


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
        endpoint, headers={'Authorization': f'Bearer {token}'}, json=payload
    )
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_registrar_recibos_sem_permissao(
    client: FlaskClient, seed_doacao_com_itens_doados
):
    doacao_id, _ = seed_doacao_com_itens_doados
    endpoint = f'{REGISTRAR_RECIBOS_BASE_ENDPOINT}/{doacao_id}'
    payload = {
        'recibos': [
            {'recibo': 'https://example.com/recibo/test_sem_permissao'}
        ]
    }

    resposta = client.post(endpoint, json=payload)
    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
