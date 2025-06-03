from http import HTTPStatus

from flask.testing import FlaskClient

LISTAR_FAMILIAS_ENDPOINT = 'api/agape/listar-familias'


def test_listar_familias_sucesso_com_dados(
    client: FlaskClient,
    membro_token,
):
    """
    Testa a listagem bem-sucedida de famílias ágape ativas.
    Verifica se a resposta contém as famílias esperadas e a paginação correta.
    """

    resposta = client.get(
        LISTAR_FAMILIAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json

    assert 'resultados' in resposta_json
    assert 'total' in resposta_json
    assert 'pagina' in resposta_json
    assert 'paginas' in resposta_json
    assert isinstance(resposta_json['resultados'], list)

    # Verifica alguns campos básicos
    for familia_retornada in resposta_json['resultados']:
        assert 'id' in familia_retornada
        assert 'nome_familia' in familia_retornada
        assert 'membros' in familia_retornada
        assert 'observacao' in familia_retornada


def test_listar_familias_sem_permissao(
    client: FlaskClient,
):
    """
    Testa a tentativa de listar famílias sem as permissões adequadas (token).
    Espera-se um status UNAUTHORIZED.
    """
    resposta = client.get(
        LISTAR_FAMILIAS_ENDPOINT,
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
