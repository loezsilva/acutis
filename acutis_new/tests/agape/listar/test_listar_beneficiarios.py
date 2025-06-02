import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

LISTAR_BENEFICIARIOS_ENDPOINT = 'api/agape/listar-beneficiarios'

def test_listar_beneficiarios_ciclo_com_doacoes_sucesso(
    client: FlaskClient,
    seed_ciclo_com_doacoes_completas,
    membro_token,
):
    """
    Testa a listagem bem-sucedida de beneficiários para um ciclo
    que possui doações.
    """
    dados_fixture = seed_ciclo_com_doacoes_completas
    ciclo_acao = dados_fixture['ciclo_acao']
    doacoes_info_esperadas = dados_fixture['doacoes_info']

    ids_familias_beneficiarias = {
        info['familia'].id for info in doacoes_info_esperadas
    }

    resposta = client.get(
        f'{LISTAR_BENEFICIARIOS_ENDPOINT}/{ciclo_acao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    assert isinstance(resposta_json, list)
    assert len(resposta_json) == len(ids_familias_beneficiarias)


def test_listar_beneficiarios_ciclo_sem_doacoes(
    client: FlaskClient,
    seed_ciclo_acao_agape,
    membro_token,
):
    """
    Testa a listagem de beneficiários para um ciclo que não possui doações.
    Espera-se uma lista vazia como resposta.
    """
    ciclo_acao_sem_doacoes = seed_ciclo_acao_agape[0]

    resposta = client.get(
        f'{LISTAR_BENEFICIARIOS_ENDPOINT}/{ciclo_acao_sem_doacoes.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    assert isinstance(resposta_json, list)
    assert (
        len(resposta_json) == 0, \
        "A lista de beneficiários deveria estar vazia"
    )


def test_listar_beneficiarios_ciclo_nao_encontrado(
    client: FlaskClient, membro_token
):
    """
    Testa a tentativa de listar beneficiários para um ID de ciclo de ação
    que não existe.
    """
    uuid_invalido = uuid.uuid4()

    resposta = client.get(
        f'{LISTAR_BENEFICIARIOS_ENDPOINT}/{uuid_invalido}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND

def test_listar_beneficiarios_sem_permissao(
    client: FlaskClient,
):
    """
    Testa a tentativa de listar beneficiários sem as permissões adequadas.
    """
    uuid_invalido = uuid.uuid4()

    resposta = client.get(
        f'{LISTAR_BENEFICIARIOS_ENDPOINT}/{uuid_invalido}',
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED