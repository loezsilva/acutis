from http import HTTPStatus

ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT = (
    'api/agape/atualizar-permissoes-voluntarios'
)


def test_atualizar_permissoes_voluntarios_sucesso(
    client,
    seed_lead_voluntario_e_token,
    seed_menu_agape_e_permissoes,
):
    token = seed_lead_voluntario_e_token[1]

    resposta = client.put(
        f'{ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert resposta.status_code == HTTPStatus.NO_CONTENT


def test_atualizar_permissoes_voluntarios_sem_permissao_rota(
    client,
    membro_token,
):
    resposta = client.put(
        f'{ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    dados_resposta = resposta.json
    assert resposta.status_code == HTTPStatus.FORBIDDEN
    assert (
        dados_resposta[0].get('msg')
        == 'Você não tem permissão para realizar esta ação.'
    )


def test_atualizar_permissoes_sem_token(client):
    resposta = client.put(
        f'{ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT}',
    )

    assert resposta.status_code == HTTPStatus.UNAUTHORIZED
