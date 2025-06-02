import uuid
from http import HTTPStatus

ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT = (
    'api/agape/atualizar-permissoes-voluntarios'
)


def test_atualizar_permissoes_voluntarios_sucesso(
    client, seed_lead_voluntario_e_token
):
    lead, token = seed_lead_voluntario_e_token
    dados_payload = {
        'atualizacoes': [
            {
                'lead_id': str(lead.id),
                'perfis_agape': [
                    'Voluntario Agape',
                ],
            }
        ]
    }

    resposta = client.put(
        f'{ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT}',
        headers={'Authorization': f'Bearer {token}'},
        json=dados_payload,
    )

    dados_resposta = resposta.json
    resultados = dados_resposta.get('resultados', [])
    assert resposta.status_code == HTTPStatus.OK
    assert len(resultados) == 1
    assert resultados[0].get('lead_id') == str(lead.id)
    assert resultados[0].get('status') == 'Atualizado com sucesso.'


def test_atualizar_permissoes_voluntarios_lead_invalido(
    client, seed_lead_voluntario_e_token
):
    membro_token = seed_lead_voluntario_e_token[1]
    dados_payload = {
        'atualizacoes': [
            {
                'lead_id': str(uuid.uuid4()),
                'perfis_agape': [
                    'Voluntario Agape',
                ],
            }
        ]
    }

    resposta = client.put(
        f'{ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_payload,
    )

    dados_resposta = resposta.json
    resultados = dados_resposta.get('resultados', [])
    assert resposta.status_code == HTTPStatus.OK
    assert len(resultados) == 1
    assert resultados[0].get('status') != 'Atualizado com sucesso.'


def test_atualizar_permissoes_voluntarios_sem_permissao_rota(
    client,
    membro_token,
):
    dados_payload = {
        'atualizacoes': [
            {
                'lead_id': uuid.uuid4(),
                'perfis_agape': [
                    'Perfil Inexistente',
                ],
            }
        ]
    }

    resposta = client.put(
        f'{ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT}',
        headers={'Authorization': f'Bearer {membro_token}'},
        json=dados_payload,
    )

    dados_resposta = resposta.json
    assert resposta.status_code == HTTPStatus.FORBIDDEN
    assert (
        dados_resposta[0].get('msg')
        == 'Você não tem permissão para realizar esta ação.'
    )


def test_atualizar_permissoes_payload_invalido(
    client, seed_lead_voluntario_e_token
):
    lead, token = seed_lead_voluntario_e_token
    dados_payload_invalido = {
        'atualizacoes': [
            {
                'atributo': lead.id,
            }
        ]
    }

    resposta = client.put(
        f'{ATUALIZAR_PERMISSOES_VOLUNTARIOS_ENDPOINT}',
        headers={'Authorization': f'Bearer {token}'},
        json=dados_payload_invalido,
    )

    assert int(resposta.status_code) in set([
        HTTPStatus.UNPROCESSABLE_ENTITY,
        HTTPStatus.BAD_REQUEST,
    ])
