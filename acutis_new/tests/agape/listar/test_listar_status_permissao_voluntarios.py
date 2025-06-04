from http import HTTPStatus
from flask.testing import FlaskClient
# Nenhuma importação direta de database ou Factory é necessária neste arquivo de teste

STATUS_PERMISSAO_ENDPOINT = '/api/agape/status-permissao-voluntarios'

def test_listar_status_permissao_voluntarios_sucesso(
    client: FlaskClient,
    membro_token,
    seed_leads_com_diversas_permissoes_agape
):
    
    dados_leads_semeados = seed_leads_com_diversas_permissoes_agape

    resposta = client.get(
        STATUS_PERMISSAO_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    
    assert 'resultados' in resposta_json
    assert 'total' in resposta_json
    assert 'pagina' in resposta_json
    assert 'paginas' in resposta_json

    leads_esperados_no_resultado = [
        v for k, v in dados_leads_semeados.items()
        if 'Voluntario Agape' in v['perfis_agape'] or
           'Administrador Agape' in v['perfis_agape']
    ]

    assert resposta_json['total'] >= len(leads_esperados_no_resultado)


    resultados_por_id = {
        item['lead_id']: item for item in resposta_json['resultados']
    }

    for lead_esperado in leads_esperados_no_resultado:
        lead_id_esperado = lead_esperado['id']
        assert lead_id_esperado in resultados_por_id, (
            f"Lead esperado com ID {lead_id_esperado} não encontrado nos "
            "resultados."
        )

        voluntario_retornado = resultados_por_id[lead_id_esperado]

        assert voluntario_retornado['nome'] == lead_esperado['nome']
        assert voluntario_retornado['email'] == lead_esperado['email']
        assert sorted(voluntario_retornado['perfis_agape']) == sorted(
            lead_esperado['perfis_agape'])

    lead_comum_info = dados_leads_semeados.get('lead_comum')
    if lead_comum_info:
        id_lead_comum = lead_comum_info.get('id')
        if id_lead_comum:
            assert id_lead_comum not in resultados_por_id, (
                f"Lead comum com ID {id_lead_comum} não deveria estar nos "
                "resultados."
            )

    if resposta_json['total'] == len(leads_esperados_no_resultado):
        assert len(resposta_json['resultados']) == len(
            leads_esperados_no_resultado)

def test_listar_status_permissao_voluntarios_sem_voluntarios_relevantes(
    client: FlaskClient,
    membro_token
):
    resposta = client.get(
        STATUS_PERMISSAO_ENDPOINT,
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert resposta.status_code == HTTPStatus.OK
    resposta_json = resposta.json
    assert resposta_json['total'] == 0

def test_listar_status_permissao_voluntarios_sem_token(client: FlaskClient):
    resposta = client.get(
        STATUS_PERMISSAO_ENDPOINT,
    )
    assert resposta.status_code == HTTPStatus.UNAUTHORIZED