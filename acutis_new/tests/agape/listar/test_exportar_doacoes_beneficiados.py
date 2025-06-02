import uuid
from http import HTTPStatus

import pandas as pd
from flask.testing import FlaskClient

EXPORTAR_DOACOES_BENEFICIADOS_ENDPOINT = (
    'api/agape/exportar-doacoes-beneficiados'
)


def test_exportar_doacoes_beneficiados_sucesso_com_dados(
    client: FlaskClient,
    seed_ciclo_com_doacoes_completas,
    membro_token,
):
    """
    Testa a exportação bem-sucedida de doações para beneficiados em CSV.
    """
    ciclo_acao = seed_ciclo_com_doacoes_completas['ciclo_acao']

    resposta = client.get(
        f'{EXPORTAR_DOACOES_BENEFICIADOS_ENDPOINT}/{ciclo_acao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    dados_resposta = resposta.json
    assert resposta.status_code == HTTPStatus.OK
    assert 'url' in dados_resposta

    url = dados_resposta['url']

    df = pd.read_excel(url)

    # Verifica se as colunas esperadas estão presentes
    colunas_esperadas = [
        'ciclo_acao_id',
        'ciclo_acao_nome',
        'ciclo_acao_data_inicio',
        'ciclo_acao_data_termino',
        'familia_id',
        'familia_nome',
        'familia_observacao',
        'responsavel_familia_nome',
        'responsavel_familia_cpf',
        'responsavel_familia_telefone',
        'doacao_id',
        'doacao_data',
        'item_doado_nome',
        'item_doado_quantidade',
    ]
    for coluna in colunas_esperadas:
        assert coluna in df.columns, f'Coluna ausente no CSV: {coluna}'


def test_exportar_doacoes_beneficiados_ciclo_sem_doacoes(
    client: FlaskClient,
    seed_ciclo_acao_agape,
    membro_token,
):
    """
    Testa a exportação de um ciclo de ação que não possui doações.
    Espera-se um CSV apenas com cabeçalhos ou vazio (conforme a implementação).
    """
    ciclo_acao = seed_ciclo_acao_agape[0]

    resposta = client.get(
        f'{EXPORTAR_DOACOES_BENEFICIADOS_ENDPOINT}/{ciclo_acao.id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    assert not resposta.json['url']


def test_exportar_doacoes_beneficiados_ciclo_nao_encontrado(
    client: FlaskClient, membro_token
):
    """
    Testa a tentativa de exportação para um ID de ciclo de ação que não existe.
    """
    uuid_invalido = uuid.uuid4()

    resposta = client.get(
        f'{EXPORTAR_DOACOES_BENEFICIADOS_ENDPOINT}/{uuid_invalido}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.NOT_FOUND


def test_exportar_doacoes_beneficiados_sem_permissao(
    client: FlaskClient,
    seed_ciclo_acao_agape,
):
    """
    Testa a tentativa de exportação sem as permissões adequadas.
    """
    ciclo_acao = seed_ciclo_acao_agape[0]

    resposta = client.get(
        f'{EXPORTAR_DOACOES_BENEFICIADOS_ENDPOINT}/{ciclo_acao.id}',
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
