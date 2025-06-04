from http import HTTPStatus
import uuid
from flask.testing import FlaskClient

REMOVER_VOLUNTARIO_ENDPOINT_BASE = '/api/agape/remover-voluntario-agape'

def test_remover_voluntario_agape_sucesso(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    membro_token
):
    
    lead_a_remover = seed_lead_voluntario_e_token[0]

    endpoint = f"{REMOVER_VOLUNTARIO_ENDPOINT_BASE}/{lead_a_remover.id}"

    resposta = client.delete(
        endpoint,
        headers={'Authorization': f'Bearer {membro_token}'}
    )

    assert resposta.status_code == HTTPStatus.NO_CONTENT

def test_remover_voluntario_agape_lead_inexistente(
    client: FlaskClient,
    membro_token
):
    
    lead_id_inexistente = uuid.uuid4()
    endpoint = f"{REMOVER_VOLUNTARIO_ENDPOINT_BASE}/{lead_id_inexistente}"

    resposta = client.delete(
        endpoint,
        headers={'Authorization': f'Bearer {membro_token}'}
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND

def test_remover_voluntario_agape_lead_nao_e_voluntario(
    client: FlaskClient,
    membro_token,
    seed_registrar_membro
):
    lead_comum, membro, _ = seed_registrar_membro(status=True)
    
    endpoint = f"{REMOVER_VOLUNTARIO_ENDPOINT_BASE}/{lead_comum.id}"

    resposta = client.delete(
        endpoint,
        headers={'Authorization': f'Bearer {membro_token}'}
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND

def test_remover_voluntario_agape_sem_permissao_token(
    client: FlaskClient,
    seed_lead_voluntario_e_token
):
    
    lead_a_remover = seed_lead_voluntario_e_token[0]
    endpoint = f"{REMOVER_VOLUNTARIO_ENDPOINT_BASE}/{lead_a_remover.id}"

    resposta = client.delete(endpoint)
    assert resposta.status_code == HTTPStatus.UNAUTHORIZED