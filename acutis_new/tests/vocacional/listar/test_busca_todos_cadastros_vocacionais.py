from datetime import datetime
from http import HTTPStatus

from faker import Faker
from flask.testing import FlaskClient

from acutis_api.communication.enums.vocacional import (
    PassosVocacionalEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.entities.cadastro_vocacional import CadastroVocacional
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.etapa_vocacional import EtapaVocacional
from acutis_api.domain.entities.usuario_vocacional import UsuarioVocacional
from acutis_api.infrastructure.extensions import database
from tests.factories import (
    EnderecoFactory,
    EtapaVocacionalFactory,
    UsuarioVocacionalFactory,
)

faker = Faker('pt_BR')


def test_busca_todos_cadastros_vocacionais(
    client: FlaskClient, membro_token, seed_cadastro_vocacional_aprovado
):
    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK

    data_response = response.get_json()

    assert 'cadastros_vocacionais' in data_response
    assert 'total' in data_response
    assert 'pagina' in data_response


def test_busca_cadastro_por_brasil(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory(pais='brasil')

    database.session.add(novo_pre_cadastro)
    database.session.flush()

    novo_endereco = EnderecoFactory()

    database.session.add(novo_endereco)
    database.session.flush()

    novo_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_pre_cadastro)
    database.session.flush()

    novo_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        fk_endereco_id=novo_endereco.id,
        data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade='20994073046',
    )

    database.session.add(novo_cadastro_vocacional)
    database.session.flush()

    novo_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.cadastro,
        status=PassosVocacionalStatusEnum.pendente,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_cadastro)

    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?pais=brasil',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    cadastro = response.json['cadastros_vocacionais'][0]['pre_cadastro']
    assert cadastro['pais'] == 'brasil'


def test_busca_cadastro_por_outros_paises(
    client: FlaskClient,
    membro_token,
    seed_cadastro_vocacional_pendente,
):
    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?pais=argentina',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK

    cadastros = response.json['cadastros_vocacionais']
    for pre_cadastro in cadastros:
        assert pre_cadastro['pre_cadastro']['pais'] != 'brasil'


def test_busca_cadastro_por_telefone(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory(telefone='83998422828')

    database.session.add(novo_pre_cadastro)
    database.session.flush()

    novo_endereco = EnderecoFactory()

    database.session.add(novo_endereco)
    database.session.flush()

    novo_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_pre_cadastro)
    database.session.flush()

    novo_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        fk_endereco_id=novo_endereco.id,
        data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade='20994073046',
    )

    database.session.add(novo_cadastro_vocacional)
    database.session.flush()

    novo_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.cadastro,
        status=PassosVocacionalStatusEnum.pendente,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_cadastro)

    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?telefone=83998422828',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    cadastro = response.json['cadastros_vocacionais'][0]['pre_cadastro']
    assert cadastro['telefone'] == '83998422828'


def test_busca_cadastro_por_status(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory()

    database.session.add(novo_pre_cadastro)
    database.session.flush()

    novo_endereco = EnderecoFactory()

    database.session.add(novo_endereco)
    database.session.flush()

    novo_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_pre_cadastro)
    database.session.flush()

    novo_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        fk_endereco_id=novo_endereco.id,
        data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade='20994073046',
    )

    database.session.add(novo_cadastro_vocacional)
    database.session.flush()

    novo_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_cadastro)

    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?status=aprovado',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    cadastro = response.json['cadastros_vocacionais'][0]['pre_cadastro']
    assert cadastro['status'] == PassosVocacionalStatusEnum.aprovado


def test_busca_cadastro_por_nome(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory(nome='João')
    database.session.add(novo_pre_cadastro)
    database.session.flush()
    novo_endereco = EnderecoFactory()
    database.session.add(novo_endereco)
    database.session.flush()
    novo_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_pre_cadastro)
    database.session.flush()

    novo_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        fk_endereco_id=novo_endereco.id,
        data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade='20994073046',
    )

    database.session.add(novo_cadastro_vocacional)
    database.session.flush()

    novo_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.cadastro,
        status=PassosVocacionalStatusEnum.pendente,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_cadastro)
    database.session.commit()

    pre_cadastro_2 = UsuarioVocacionalFactory(nome='Maria')
    database.session.add(pre_cadastro_2)
    database.session.flush()
    endereco_2 = EnderecoFactory()
    database.session.add(endereco_2)
    database.session.flush()
    etapa_pre_cadastro_2 = EtapaVocacional(
        fk_usuario_vocacional_id=pre_cadastro_2.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(etapa_pre_cadastro_2)
    database.session.flush()

    cadastro_vocacional_2 = CadastroVocacional(
        fk_usuario_vocacional_id=pre_cadastro_2.id,
        fk_endereco_id=novo_endereco.id,
        data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade='20992343046',
    )

    database.session.add(cadastro_vocacional_2)
    database.session.flush()

    etapa_cadastro_2 = EtapaVocacional(
        fk_usuario_vocacional_id=pre_cadastro_2.id,
        etapa=PassosVocacionalEnum.cadastro,
        status=PassosVocacionalStatusEnum.pendente,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(etapa_cadastro_2)
    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?nome=Maria',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    cadastro = response.json['cadastros_vocacionais'][0]['pre_cadastro']
    assert cadastro['nome'] == 'Maria'


def test_busca_cadastro_por_email(client: FlaskClient, membro_token):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory(email='teste@gmail.com')

    database.session.add(novo_pre_cadastro)
    database.session.flush()

    novo_endereco = EnderecoFactory()

    database.session.add(novo_endereco)
    database.session.flush()

    novo_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_pre_cadastro)
    database.session.flush()

    novo_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        fk_endereco_id=novo_endereco.id,
        data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade='20994073046',
    )

    database.session.add(novo_cadastro_vocacional)
    database.session.flush()

    novo_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.cadastro,
        status=PassosVocacionalStatusEnum.pendente,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_cadastro)

    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?email=teste@gmail.com',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    cadastro = response.json['cadastros_vocacionais'][0]['pre_cadastro']
    assert cadastro['email'] == 'teste@gmail.com'


def test_busca_cadastro_por_data_inicial(
    client: FlaskClient,
    membro_token,
    mock_db_time,
    seed_cadastro_vocacional_pendente,
):
    total_registros = 1

    with mock_db_time(model=UsuarioVocacional, time=datetime(2035, 3, 11)):
        pre_cadastro_2 = UsuarioVocacionalFactory(nome='João')
        database.session.add(pre_cadastro_2)
        database.session.flush()

    with mock_db_time(model=Endereco, time=datetime(2035, 3, 11)):
        endereco_2 = EnderecoFactory()
        database.session.add(endereco_2)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2035, 3, 11)):
        etapa_2 = EtapaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro_2.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.aprovado,
        )
        database.session.add(etapa_2)
        database.session.commit()

    with mock_db_time(model=CadastroVocacional, time=datetime(2035, 3, 11)):
        cadastro_2 = CadastroVocacional(
            fk_usuario_vocacional_id=pre_cadastro_2.id,
            fk_endereco_id=endereco_2.id,
            data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
            documento_identidade='20994073046',
        )

        database.session.add(cadastro_2)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2035, 3, 11)):
        etapa_cadastro_2 = EtapaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro_2.id,
            etapa=PassosVocacionalEnum.cadastro,
            status=PassosVocacionalStatusEnum.pendente,
        )

        database.session.add(etapa_cadastro_2)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?data_inicial=2035-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    cadastro = response.json['cadastros_vocacionais'][0]['pre_cadastro']
    assert cadastro['nome'] == 'João'


def test_busca_cadastro_por_data_final(
    client: FlaskClient,
    membro_token,
    mock_db_time,
    seed_cadastro_vocacional_pendente,
):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory()
    database.session.add(novo_pre_cadastro)
    database.session.flush()

    etapa = EtapaVocacionalFactory(
        fk_usuario_vocacional_id=novo_pre_cadastro.id
    )
    database.session.add(etapa)
    database.session.commit()

    with mock_db_time(model=UsuarioVocacional, time=datetime(2023, 3, 11)):
        pre_cadastro_2 = UsuarioVocacionalFactory(nome='João')
        database.session.add(pre_cadastro_2)
        database.session.flush()

    with mock_db_time(model=Endereco, time=datetime(2023, 3, 11)):
        endereco_2 = EnderecoFactory()
        database.session.add(endereco_2)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2023, 3, 11)):
        etapa_2 = EtapaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro_2.id,
            etapa=PassosVocacionalEnum.pre_cadastro,
            status=PassosVocacionalStatusEnum.aprovado,
        )
        database.session.add(etapa_2)
        database.session.commit()

    with mock_db_time(model=CadastroVocacional, time=datetime(2023, 3, 11)):
        cadastro_2 = CadastroVocacional(
            fk_usuario_vocacional_id=pre_cadastro_2.id,
            fk_endereco_id=endereco_2.id,
            data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
            documento_identidade='20994073046',
        )

        database.session.add(cadastro_2)
        database.session.flush()

    with mock_db_time(model=EtapaVocacional, time=datetime(2023, 3, 11)):
        etapa_cadastro_2 = EtapaVocacionalFactory(
            fk_usuario_vocacional_id=pre_cadastro_2.id,
            etapa=PassosVocacionalEnum.cadastro,
            status=PassosVocacionalStatusEnum.pendente,
        )

        database.session.add(etapa_cadastro_2)
        database.session.commit()

    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?data_final=2024-03-10',
        headers={'Authorization': f'Bearer {membro_token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros

    cadastro = response.json['cadastros_vocacionais'][0]['pre_cadastro']
    assert cadastro['nome'] == 'João'


def test_busca_cadastro_por_documento(
    client: FlaskClient,
    membro_token,
):
    total_registros = 1

    novo_pre_cadastro = UsuarioVocacionalFactory()

    database.session.add(novo_pre_cadastro)
    database.session.flush()

    novo_endereco = EnderecoFactory()

    database.session.add(novo_endereco)
    database.session.flush()

    novo_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.pre_cadastro,
        status=PassosVocacionalStatusEnum.aprovado,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_pre_cadastro)
    database.session.flush()

    novo_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        fk_endereco_id=novo_endereco.id,
        data_nascimento=datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade='20994072546',
    )

    database.session.add(novo_cadastro_vocacional)
    database.session.flush()

    novo_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=novo_pre_cadastro.id,
        etapa=PassosVocacionalEnum.cadastro,
        status=PassosVocacionalStatusEnum.pendente,
        justificativa=None,
        fk_responsavel_id=None,
    )

    database.session.add(novo_etapa_cadastro)

    database.session.commit()

    response = client.get(
        '/api/vocacional/listar-cadastros-vocacionais?documento_identidade=20994072546',
        headers={'Authorization': f'Bearer {membro_token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json['total'] == total_registros
    cadastro = response.json['cadastros_vocacionais'][0]['cadastro_vocacional']
    assert cadastro['documento_identidade'] == '20994072546'
