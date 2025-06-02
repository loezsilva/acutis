from http import HTTPStatus

import pandas as pd
from flask.testing import FlaskClient

EXPORTAR_FAMILIAS_ENDPOINT = 'api/agape/exportar-familias'


def test_exportar_familias_sucesso_com_dados(
    client: FlaskClient,
    seed_diversas_familias_para_exportacao,
    membro_token,
):
    """
    Testa a exportação bem-sucedida de múltiplas famílias Ágape em CSV.
    """

    response = client.get(
        EXPORTAR_FAMILIAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    dados_resposta = response.json
    assert response.status_code == HTTPStatus.OK
    assert 'url' in dados_resposta

    url = dados_resposta['url']
    df = pd.read_excel(url)

    # Verifica se as colunas esperadas estão presentes
    colunas_esperadas = [
        'familia_id',
        'familia_nome',
        'familia_data_cadastro',
        'familia_status',
        'familia_observacao',
        'endereco_logradouro',
        'endereco_numero',
        'endereco_complemento',
        'endereco_bairro',
        'endereco_cidade',
        'endereco_estado',
        'endereco_cep',
        'responsavel_nome',
        'responsavel_cpf',
        'responsavel_telefone',
        'responsavel_email',
        'responsavel_data_nascimento',
        'responsavel_funcao_familiar',
        'responsavel_escolaridade',
        'responsavel_ocupacao',
        'numero_total_membros',
        'renda_familiar_total_estimada',
        'comprovante_residencia_url',
        'cadastrada_por_usuario_id',
    ]
    for coluna in colunas_esperadas:
        assert coluna in df.columns, f'Coluna ausente no CSV: {coluna}'


def test_exportar_familias_sem_dados(
    client: FlaskClient,
    membro_token,
):
    """
    Testa a exportação quando não há famílias cadastradas.
    Espera-se um CSV apenas com cabeçalhos.
    """

    response = client.get(
        EXPORTAR_FAMILIAS_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert not response.json['url']


def test_exportar_familias_sem_permissao(
    client: FlaskClient,
):
    """
    Testa a tentativa de exportação de famílias sem as permissões adequadas.
    """

    response = client.get(
        EXPORTAR_FAMILIAS_ENDPOINT,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
