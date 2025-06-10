import uuid
from http import HTTPStatus

from flask.testing import FlaskClient

LISTAR_MEMBROS_FAMILIA_ENDPOINT_TEMPLATE = (
    'api/agape/listar-membros-familia/{}'
)


def test_listar_membros_familia_sucesso(
    client: FlaskClient,
    seed_familia_com_membros_e_rendas,
    membro_token: str,
):
    """
    Testa a listagem bem-sucedida de membros de uma família existente.
    Verifica o status da resposta, a contagem total de membros,
    a paginação e os detalhes dos membros retornados.
    """
    familia_criada = seed_familia_com_membros_e_rendas[0]
    url = LISTAR_MEMBROS_FAMILIA_ENDPOINT_TEMPLATE.format(familia_criada.id)

    resposta = client.get(
        url, headers={'Authorization': f'Bearer {membro_token}'}
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json

    assert resposta_json['total'] > 0
    assert len(resposta_json['resultados']) > 0
    assert resposta_json['pagina'] == 1
    assert resposta_json['paginas'] == 1


def test_listar_membros_familia_id_nao_encontrado(
    client: FlaskClient, membro_token: str
):
    """
    Testa a listagem de membros para um familia_id que não existe.
    Espera-se uma resposta OK com a lista de resultados vazia.
    """
    familia_id_inexistente = uuid.uuid4()
    url = LISTAR_MEMBROS_FAMILIA_ENDPOINT_TEMPLATE.format(
        familia_id_inexistente
    )

    resposta = client.get(
        url, headers={'Authorization': f'Bearer {membro_token}'}
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_listar_membros_familia_sem_permissao(
    client: FlaskClient,
    seed_familia_com_membros_e_rendas,
):
    """
    Testa a tentativa de listar membros sem token de autenticação.
    Espera-se uma resposta de NÃO AUTORIZADO.
    """
    familia_criada = seed_familia_com_membros_e_rendas[0]
    url = LISTAR_MEMBROS_FAMILIA_ENDPOINT_TEMPLATE.format(familia_criada.id)

    resposta = client.get(url)  # Sem header de autorização

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED


def test_listar_membros_familia_id_formato_invalido(
    client: FlaskClient, membro_token: str
):
    """
    Testa a listagem com um familia_id de formato inválido.
    Espera-se 404 NOT_FOUND ou 422 UNPROCESSABLE_ENTITY.
    """
    familia_id_invalido = 'id-nao-uuid'
    url = LISTAR_MEMBROS_FAMILIA_ENDPOINT_TEMPLATE.format(familia_id_invalido)

    resposta = client.get(
        url, headers={'Authorization': f'Bearer {membro_token}'}
    )

    assert resposta.status_code in set([
        HTTPStatus.NOT_FOUND,
        HTTPStatus.UNPROCESSABLE_ENTITY,
    ])
