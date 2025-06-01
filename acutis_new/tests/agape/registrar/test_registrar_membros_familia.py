import datetime
import uuid
from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

REGISTRAR_MEMBROS_ENDPOINT = '/api/agape/registrar-membros/{familia_agape_id}'

faker = Faker('pt_BR')


def _gerar_payload_membro_valido(responsavel=False, cpf='184.860.290-15'):
    """Gera um dicionário com dados válidos para um membro."""
    data_nascimento = datetime.date.today() - datetime.timedelta(days=365 * 20)
    return {
        'email': faker.email(),
        'telefone': faker.phone_number(),
        'nome': faker.name(),
        'cpf': cpf if cpf else faker.cpf(),
        'data_nascimento': data_nascimento.isoformat(),
        'funcao_familiar': 'Filho(a)',
        'escolaridade': 'Ensino Médio Completo',
        'ocupacao': faker.job(),
        'renda': float(faker.random_number(digits=4)),
        'beneficiario_assistencial': faker.boolean(),
        'responsavel': responsavel,
        'foto_documento': None,
    }


def test_registrar_membros_familia_sucesso(
    client: FlaskClient, membro_token, seed_familia_com_endereco
):
    """Testa o registro bem-sucedido de membros em uma família."""
    familia = seed_familia_com_endereco[0]
    payload = {
        'membros': [
            _gerar_payload_membro_valido(responsavel=True),
            _gerar_payload_membro_valido(cpf=None),
        ]
    }

    response = client.post(
        REGISTRAR_MEMBROS_ENDPOINT.format(familia_agape_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json
    assert 'msg' in response_data


def test_registrar_membros_familia_id_familia_inexistente(
    client: FlaskClient, membro_token
):
    """Testa registrar membros para um ID de família inexistente."""
    id_familia_inexistente = uuid.uuid4()
    payload = {'membros': [_gerar_payload_membro_valido()]}

    response = client.post(
        REGISTRAR_MEMBROS_ENDPOINT.format(
            familia_agape_id=id_familia_inexistente
        ),
        headers={'Authorization': f'Bearer {membro_token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_registrar_membros_payload_invalido_sem_membros(
    client: FlaskClient, membro_token, seed_familia_com_endereco
):
    """Testa registrar membros com payload inválido."""
    familia = seed_familia_com_endereco[0]
    payload = {'membros': []}

    response = client.post(
        REGISTRAR_MEMBROS_ENDPOINT.format(familia_agape_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
        json=payload,
    )

    assert int(response.status_code) == HTTPStatus.BAD_REQUEST


def test_registrar_membros_payload_invalido_campo_obrigatorio_faltando(
    client: FlaskClient, membro_token, seed_familia_com_endereco
):
    """Testa registrar membros com campo obrigatório faltando (ex: nome)."""
    familia = seed_familia_com_endereco[0]
    membro_sem_nome = _gerar_payload_membro_valido()
    del membro_sem_nome['nome']
    payload = {'membros': [membro_sem_nome]}

    response = client.post(
        REGISTRAR_MEMBROS_ENDPOINT.format(familia_agape_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    response_data = response.json
    assert isinstance(response_data, list)
    assert len(response_data) > 0
    assert response_data[0]['loc'][0] == 'membros'
    assert response_data[0]['loc'][2] == 'nome'
    assert response_data[0]['type'] == 'missing'


def test_registrar_membro_cpf_duplicado_na_mesma_requisicao(
    client: FlaskClient, membro_token, seed_familia_com_endereco
):
    """Testa registrar dois membros com o mesmo CPF na mesma requisição."""
    familia = seed_familia_com_endereco[0]
    membro1 = _gerar_payload_membro_valido()
    membro2 = _gerar_payload_membro_valido()

    payload = {'membros': [membro1, membro2]}

    response = client.post(
        REGISTRAR_MEMBROS_ENDPOINT.format(familia_agape_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
        json=payload,
    )

    assert int(response.status_code) == HTTPStatus.CONFLICT


def test_registrar_membro_email_duplicado_na_mesma_requisicao(
    client: FlaskClient, membro_token, seed_familia_com_endereco
):
    """Testa registrar dois membros com o mesmo CPF na mesma requisição."""
    familia = seed_familia_com_endereco[0]
    membro1 = _gerar_payload_membro_valido()
    membro1['email'] = 'lucilene.norte@geradornv.com.br'
    membro2 = _gerar_payload_membro_valido()
    membro2['email'] = 'lucilene.norte@geradornv.com.br'

    payload = {'membros': [membro1, membro2]}

    response = client.post(
        REGISTRAR_MEMBROS_ENDPOINT.format(familia_agape_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
        json=payload,
    )

    assert int(response.status_code) == HTTPStatus.CONFLICT


def test_registrar_membro_cpf_ja_existente_em_outra_familia(
    client: FlaskClient,
    membro_token,
    seed_familia_com_endereco,
    seed_membro_agape,
):
    """Testa registrar membro com CPF que já existe em outra família."""
    familia = seed_familia_com_endereco[0]
    membro_existente = seed_membro_agape
    payload_novo_membro = _gerar_payload_membro_valido()
    payload_novo_membro['cpf'] = membro_existente.cpf
    payload = {'membros': [payload_novo_membro]}

    response = client.post(
        REGISTRAR_MEMBROS_ENDPOINT.format(familia_agape_id=familia.id),
        headers={'Authorization': f'Bearer {membro_token}'},
        json=payload,
    )

    assert int(response.status_code) == HTTPStatus.CONFLICT
