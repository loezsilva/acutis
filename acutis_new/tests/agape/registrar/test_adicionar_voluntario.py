from http import HTTPStatus
import uuid

ADICIONAR_VOLUNTARIO_ENDPOINT = 'api/agape/adicionar-voluntario'

def test_adicionar_voluntario_sucesso(
    client, 
    seed_lead_voluntario_e_token
):
    lead, token = seed_lead_voluntario_e_token
    response = client.put(
        f'{ADICIONAR_VOLUNTARIO_ENDPOINT}/{lead.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    dados = response.json
    assert response.status_code == HTTPStatus.OK
    assert dados.get('msg') == 'Voluntário adicionado com sucesso.'

def test_adicionar_voluntario_lead_invalido(
        client, 
        seed_lead_voluntario_e_token
):
    lead_id_invalido = uuid.uuid4()
    lead, token = seed_lead_voluntario_e_token

    response = client.put(
        f'{ADICIONAR_VOLUNTARIO_ENDPOINT}/{lead_id_invalido}',
        headers={'Authorization': f'Bearer {token}'},
    )

    dados = response.json[0]
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert dados.get('msg') == 'Usuário não encontrado.'

def test_adicionar_voluntario_sem_permissao(
    client, 
    membro_token,
):
    lead_id = uuid.uuid4()

    response = client.put(
        f'{ADICIONAR_VOLUNTARIO_ENDPOINT}/{lead_id}',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    dados = response.json[0]
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert dados.get('msg') == 'Você não tem permissão para realizar esta ação.'