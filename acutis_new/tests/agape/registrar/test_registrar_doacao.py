import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

REGISTRAR_DOACAO_ENDPOINT = '/api/agape/registrar-doacao'


def test_registrar_doacao_sucesso(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_familia_com_endereco,
    seed_ciclo_acao_com_itens,
):
    token = seed_lead_voluntario_e_token[1]
    familia_agape = seed_familia_com_endereco[0]
    ciclo_acao, itens_instancia_disponiveis = seed_ciclo_acao_com_itens

    item_para_doar = itens_instancia_disponiveis[0]

    quantidade_a_doar = 1

    payload = {
        'familia_id': str(familia_agape.id),
        'ciclo_acao_id': str(ciclo_acao.id),
        'doacoes': [
            {
                'item_instancia_id': str(item_para_doar.id),
                'quantidade': quantidade_a_doar,
            }
        ],
    }

    resposta = client.post(
        REGISTRAR_DOACAO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    assert resposta.status_code == HTTPStatus.CREATED

    resposta_json = resposta.json

    assert 'doacao_id' in resposta_json
    assert 'msg' in resposta_json


def test_registrar_doacao_familia_inexistente(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_ciclo_acao_com_itens,
):
    token = seed_lead_voluntario_e_token[1]
    ciclo_acao, itens_instancia_disponiveis = seed_ciclo_acao_com_itens

    item_para_doar = itens_instancia_disponiveis[0]
    quantidade_a_doar = 1

    payload = {
        'familia_id': str(uuid.uuid4()),
        'ciclo_acao_id': str(ciclo_acao.id),
        'doacoes': [
            {
                'item_instancia_id': str(item_para_doar.id),
                'quantidade': quantidade_a_doar,
            }
        ],
    }

    resposta = client.post(
        REGISTRAR_DOACAO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_registrar_doacao_ciclo_acao_inexistente(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_familia_com_endereco,
):
    token = seed_lead_voluntario_e_token[1]
    familia_agape = seed_familia_com_endereco[0]

    payload = {
        'familia_id': str(familia_agape.id),
        'ciclo_acao_id': str(uuid.uuid4()),  # Ciclo de Ação ID aleatório
        'doacoes': [
            {
                'item_instancia_id': str(uuid.uuid4()),  # Item dummy
                'quantidade': 1,
            }
        ],
    }

    resposta = client.post(
        REGISTRAR_DOACAO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_registrar_doacao_item_instancia_inexistente(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_familia_com_endereco,
    seed_ciclo_acao_com_itens,
):
    token = seed_lead_voluntario_e_token[1]
    familia_agape = seed_familia_com_endereco[0]
    ciclo_acao, _ = seed_ciclo_acao_com_itens

    payload = {
        'familia_id': str(familia_agape.id),
        'ciclo_acao_id': str(ciclo_acao.id),
        'doacoes': [
            {
                # Item Instancia ID aleatório
                'item_instancia_id': str(uuid.uuid4()),
                'quantidade': 1,
            }
        ],
    }

    resposta = client.post(
        REGISTRAR_DOACAO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )
    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_registrar_doacao_quantidade_insuficiente(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_familia_com_endereco,
    seed_ciclo_acao_com_itens,
):
    token = seed_lead_voluntario_e_token[1]
    familia_agape = seed_familia_com_endereco[0]
    ciclo_acao, itens_instancia_disponiveis = seed_ciclo_acao_com_itens

    item_para_doar = itens_instancia_disponiveis[0]
    quantidade_a_doar = item_para_doar.quantidade + 1

    payload = {
        'familia_id': str(familia_agape.id),
        'ciclo_acao_id': str(ciclo_acao.id),
        'doacoes': [
            {
                'item_instancia_id': str(item_para_doar.id),
                'quantidade': quantidade_a_doar,
            }
        ],
    }

    resposta = client.post(
        REGISTRAR_DOACAO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    assert resposta.status_code in set([
        HTTPStatus.BAD_REQUEST,
        HTTPStatus.UNPROCESSABLE_ENTITY,
    ])


def test_registrar_doacao_payload_invalido_sem_itens(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_familia_com_endereco,
    seed_ciclo_acao_com_itens,
):
    token = seed_lead_voluntario_e_token[1]
    familia_agape = seed_familia_com_endereco[0]
    ciclo_acao, _ = seed_ciclo_acao_com_itens

    payload = {
        'familia_id': str(familia_agape.id),
        'ciclo_acao_id': str(ciclo_acao.id),
        'doacoes': [],  # Lista de itens vazia
    }

    resposta = client.post(
        REGISTRAR_DOACAO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_registrar_doacao_payload_invalido_quantidade_zero(
    client: FlaskClient,
    seed_lead_voluntario_e_token,
    seed_familia_com_endereco,
    seed_ciclo_acao_com_itens,
):
    token = seed_lead_voluntario_e_token[1]
    familia_agape = seed_familia_com_endereco[0]
    ciclo_acao, itens_instancia_disponiveis = seed_ciclo_acao_com_itens

    item_para_doar = itens_instancia_disponiveis[0]

    payload = {
        'familia_id': str(familia_agape.id),
        'ciclo_acao_id': str(ciclo_acao.id),
        'doacoes': [
            {
                'item_instancia_id': str(item_para_doar.id),
                'quantidade': 0,  # Quantidade zero
            }
        ],
    }

    resposta = client.post(
        REGISTRAR_DOACAO_ENDPOINT,
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )
    assert resposta.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_registrar_doacao_sem_permissao(
    client: FlaskClient, seed_familia_com_endereco, seed_ciclo_acao_com_itens
):
    familia_agape = seed_familia_com_endereco[0]
    ciclo_acao, itens_instancia_disponiveis = seed_ciclo_acao_com_itens

    item_para_doar = itens_instancia_disponiveis[0]
    quantidade_a_doar = 1

    payload = {
        'familia_id': str(familia_agape.id),
        'ciclo_acao_id': str(ciclo_acao.id),
        'doacoes': [
            {
                'item_instancia_id': str(item_para_doar.id),
                'quantidade': quantidade_a_doar,
            }
        ],
    }

    resposta = client.post(
        REGISTRAR_DOACAO_ENDPOINT,
        json=payload,  # Sem header de Authorization
    )
    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
