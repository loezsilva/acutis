import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import event
from testcontainers.mssql import SqlServerContainer

from acutis_api.api.app import create_app
from acutis_api.application.utils.funcoes_auxiliares import buscar_data_valida
from acutis_api.communication.enums.campanhas import (
    PeriodicidadePainelCampanhasEnum,
)
from acutis_api.communication.enums.membros import OrigemCadastroEnum, SexoEnum
from acutis_api.domain.entities.campanha import Campanha, ObjetivosCampanhaEnum
from acutis_api.domain.entities.campo_adicional import TiposCampoEnum
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.instancia_acao_agape import StatusAcaoAgapeEnum
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.infrastructure.extensions import database
from acutis_api.infrastructure.settings import TestingConfig
from tests.factories import (
    AudienciaFactory,
    BenfeitorFactory,
    CampanhaDoacaoFactory,
    CampanhaFactory,
    CampanhaMembroOficialFactory,
    CampoAdicionalFactory,
    CargoOficialGeneralFactory,
    CargoOficialMarechalFactory,
    CargosOficiaisFactory,
    CicloAcaoAgapeFactory,
    DoacaoFactory,
    EnderecoFactory,
    EstoqueAgapeFactory,
    LandingPageFactory,
    LeadCampanhaFactory,
    LeadFactory,
    LiveAvulsaFactory,
    LiveFactory,
    LiveRecorrenteFactory,
    MembroFactory,
    MembroOficialFactory,
    MetadadoLeadFactory,
    NomeAcaoAgapeFactory,
    PagamentoDoacaoFactory,
    ProcessamentoDoacaoFactory,
    PerfilFactory,
    PermissaoLeadFactory,
)
from acutis_api.domain.entities.perfil import Perfil


@pytest.fixture(scope='session')
def engine():
    container = SqlServerContainer(
        'mcr.microsoft.com/mssql/server:2022-latest', dialect='mssql+pyodbc'
    )
    container.with_env('TZ', 'America/Fortaleza')

    with container as mssql:
        yield mssql.get_connection_url()


@pytest.fixture
def app(engine):
    TestingConfig.set_test_config(engine)
    app = create_app(TestingConfig)

    with app.app_context():
        database.create_all()

        yield app

        database.drop_all()


@pytest.fixture
def client(app: Flask):
    return app.test_client()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'criado_em'):
            target.criado_em = time
        if hasattr(target, 'atualizado_em'):
            target.atualizado_em = time
        if hasattr(target, 'ultimo_acesso'):
            target.ultimo_acesso = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def seed_registrar_membro():
    def _registrar_membro(
        status: bool = False,
        nome: str | None = None,
        numero_documento: str | None = None,
        telefone: str | None = None,
        criado_em: datetime | None = None,
    ):
        lead = LeadFactory(status=status)
        lead.senha = '#Teste;@123'  # NOSONAR
        lead.origem_cadastro = OrigemCadastroEnum.acutis
        if nome:
            lead.nome = nome
        if telefone:
            lead.telefone = telefone
        if criado_em:
            lead.criado_em = criado_em
        database.session.add(lead)

        endereco = EnderecoFactory()
        database.session.add(endereco)

        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
            sexo=SexoEnum.masculino,
            data_nascimento='2004-01-01',
        )
        if numero_documento:
            membro.numero_documento = numero_documento
        else:
            membro.numero_documento = ''.join(
                filter(str.isdigit, membro.numero_documento)
            )
        if criado_em:
            membro.criado_em = criado_em
        database.session.add(membro)
        database.session.commit()

        return lead, membro, endereco

    return _registrar_membro


@pytest.fixture
def membro_token(client: FlaskClient, seed_registrar_membro):
    lead = seed_registrar_membro(status=True)[0]
    payload = {'email': lead.email, 'senha': '#Teste;@123'}

    response = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )

    return response.get_json()['access_token']


@pytest.fixture
def seed_campanha_doacao(seed_registrar_membro) -> Campanha:
    membro = seed_registrar_membro(status=True)[1]

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao,
        criado_por=membro.id,
        capa=f'{str(uuid.uuid4())}.jpg',
    )
    database.session.add(campanha)

    campanha_doacao = CampanhaDoacaoFactory(fk_campanha_id=campanha.id)
    database.session.add(campanha_doacao)

    landing_page = LandingPageFactory(fk_campanha_id=campanha.id)
    database.session.add(landing_page)

    database.session.commit()

    return campanha


@pytest.fixture
def seed_campanha_cadastro(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro, criado_por=membro.id
    )
    database.session.add(campanha_cadastro)

    landing_page = LandingPageFactory(fk_campanha_id=campanha_cadastro.id)
    database.session.add(landing_page)

    campo_adicional_1 = CampoAdicionalFactory(
        fk_campanha_id=campanha_cadastro.id,
        tipo_campo=TiposCampoEnum.string,
        nome_campo='Nome Completo',  # NOSONAR
        obrigatorio=True,
    )
    database.session.add(campo_adicional_1)

    campo_adicional_2 = CampoAdicionalFactory(
        fk_campanha_id=campanha_cadastro.id,
        tipo_campo=TiposCampoEnum.string,
        nome_campo='Email',
        obrigatorio=True,
    )
    database.session.add(campo_adicional_2)

    database.session.commit()

    return campanha_cadastro


@pytest.fixture
def seed_campanha_membros_oficiais(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    cargo_oficial = CargosOficiaisFactory(criado_por=membro.id)

    database.session.add(cargo_oficial)
    database.session.commit()

    campanha_oficiais = CampanhaMembroOficialFactory(
        criado_por=membro.id, fk_cargo_oficial_id=cargo_oficial.id
    )
    database.session.add(campanha_oficiais)

    landing_page = LandingPageFactory(fk_campanha_id=campanha_oficiais.id)
    database.session.add(landing_page)

    campo_adicional_1 = CampoAdicionalFactory(
        fk_campanha_id=campanha_oficiais.id,
        tipo_campo=TiposCampoEnum.string,
        nome_campo='Nome Completo',
        obrigatorio=True,
    )
    database.session.add(campo_adicional_1)

    campo_adicional_2 = CampoAdicionalFactory(
        fk_campanha_id=campanha_oficiais.id,
        tipo_campo=TiposCampoEnum.string,
        nome_campo='Email',
        obrigatorio=True,
    )
    database.session.add(campo_adicional_2)

    database.session.commit()

    return campanha_oficiais


@pytest.fixture
def seed_campanha_pre_cadastro_com_landing_page(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    campanha_pre_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.pre_cadastro, criado_por=membro.id
    )
    database.session.add(campanha_pre_cadastro)

    landing_page = LandingPageFactory(fk_campanha_id=campanha_pre_cadastro.id)
    database.session.add(landing_page)

    database.session.commit()

    return campanha_pre_cadastro


@pytest.fixture
def seed_nova_campanha(seed_registrar_membro):
    def _nova_campanha(publica: bool = True, ativa: bool = True):
        membro = seed_registrar_membro(status=True)[1]

        campanha = CampanhaFactory(
            publica=publica, ativa=ativa, criado_por=membro.id
        )
        database.session.add(campanha)
        database.session.commit()

        return campanha

    return _nova_campanha


@pytest.fixture
def seed_nova_campanha_com_campos_adicionais(seed_registrar_membro):
    def _nova_campanha_com_campos_adicionais(
        tipos_campos_adicionais: list[dict],
        objetivo_campanha: ObjetivosCampanhaEnum | None = None,
    ):
        membro = seed_registrar_membro(status=True)[1]

        campanha = CampanhaFactory(criado_por=membro.id)
        database.session.add(campanha)

        if objetivo_campanha == ObjetivosCampanhaEnum.doacao:
            campanha_doacao = CampanhaDoacaoFactory(
                fk_campanha_id=campanha.id,
            )
            database.session.add(campanha_doacao)

        campos_adicionais = []
        for campo in tipos_campos_adicionais:
            campo_adicional = CampoAdicionalFactory(
                fk_campanha_id=campanha.id,
                tipo_campo=campo['tipo_campo'],
                obrigatorio=campo['obrigatorio'],
            )
            campos_adicionais.append(campo_adicional)
        database.session.add_all(campos_adicionais)
        database.session.commit()

        return campanha, campos_adicionais

    return _nova_campanha_com_campos_adicionais


@pytest.fixture
def seed_cargo_oficial(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    cargo_oficial = CargosOficiaisFactory(criado_por=membro.id)

    database.session.add(cargo_oficial)

    database.session.commit()

    return cargo_oficial


@pytest.fixture
def seed_3_cargos_oficiais(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    cargos_oficiais_list = []
    for _ in range(3):
        cargo_oficial = CargosOficiaisFactory(criado_por=membro.id)
        database.session.add(cargo_oficial)
        cargos_oficiais_list.append(cargo_oficial)

    database.session.commit()

    return cargos_oficiais_list


@pytest.fixture
def seed_membros_oficial(seed_registrar_membro, seed_cargo_oficial):
    membros_oficiais_list = []

    superior = seed_registrar_membro(status=True)[1]

    for _ in range(6):
        membro = seed_registrar_membro(status=True)[1]

        membro_oficial = MembroOficialFactory(
            fk_membro_id=membro.id,
            fk_superior_id=superior.id,
            fk_cargo_oficial_id=seed_cargo_oficial.id,
            atualizado_por=None,
        )

        database.session.add(membro_oficial)
        membros_oficiais_list.append(membro_oficial)

    database.session.commit()

    membros_oficiais_list[0].criado_em = datetime(
        2025, 1, 8, 19, 23, 13, 390000
    )
    membros_oficiais_list[1].criado_em = datetime(
        2025, 1, 8, 19, 23, 13, 390000
    )

    return membros_oficiais_list


@pytest.fixture
def seed_registra_13_leads():
    leads = []
    for _ in range(12):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'
        database.session.add(lead)
        leads.append(lead)

    leads[0].criado_em = datetime(2025, 1, 8, 19, 23, 13, 390000)
    leads[1].criado_em = datetime(2025, 1, 8, 19, 23, 13, 390000)

    database.session.commit()

    return leads


@pytest.fixture
def seed_10_benfeitores():
    benfeitores = []
    for _ in range(10):
        benfeitor = BenfeitorFactory()

        database.session.add(benfeitor)

        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'
        database.session.add(lead)

        endereco = EnderecoFactory()
        database.session.add(endereco)

        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
            fk_benfeitor_id=benfeitor.id,
        )
        database.session.add(membro)

        benfeitores.append(benfeitor)
    database.session.commit()

    return benfeitores


@pytest.fixture
def seed_registra_10_membros():
    membros = []
    for _ in range(10):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'
        database.session.add(lead)

        endereco = EnderecoFactory()
        database.session.add(endereco)

        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
        )
        database.session.add(membro)
        membros.append(membro)

    membros[0].criado_em = datetime(2025, 1, 8, 19, 23, 13, 390000)
    membros[1].criado_em = datetime(2025, 1, 8, 19, 23, 13, 390000)
    database.session.commit()

    return membros


@pytest.fixture
def seed_membros_oficial_status_dinamico(
    seed_cargo_oficial, seed_registrar_membro
):
    def _criar_membro_oficial(
        status: str,
        nome: str | None = None,
        numero_documento: str | None = None,
    ):
        if nome:
            membro = seed_registrar_membro(status=True, nome=nome)[1]
        elif numero_documento:
            membro = seed_registrar_membro(
                status=True, numero_documento=numero_documento
            )[1]
        else:
            membro = seed_registrar_membro(status=True)[1]

        membro_oficial = MembroOficialFactory(
            fk_membro_id=membro.id,
            fk_cargo_oficial_id=seed_cargo_oficial.id,
            fk_superior_id=None,
            status=status,
        )

        database.session.add(membro_oficial)
        database.session.commit()
        return membro_oficial

    return _criar_membro_oficial


@pytest.fixture
def seed_cargo_oficial_general(
    seed_registrar_membro, seed_cargo_oficial_marechal
):
    membro = seed_registrar_membro(status=True)[1]

    cargo_oficial = CargoOficialGeneralFactory(
        criado_por=membro.id,
        fk_cargo_superior_id=seed_cargo_oficial_marechal.id,
    )

    database.session.add(cargo_oficial)
    database.session.commit()

    return cargo_oficial


@pytest.fixture
def seed_cargo_oficial_marechal(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    cargo_oficial = CargoOficialMarechalFactory(
        criado_por=membro.id,
        fk_cargo_superior_id=None,
    )

    database.session.add(cargo_oficial)
    database.session.commit()

    return cargo_oficial


@pytest.fixture
def seed_membros_oficial_general_status_dinamico(
    seed_cargo_oficial_general, seed_registrar_membro
):
    def _criar_membro_oficial(status: str):
        membro = seed_registrar_membro(status=True)[1]

        membro_oficial = MembroOficialFactory(
            fk_membro_id=membro.id,
            fk_cargo_oficial_id=seed_cargo_oficial_general.id,
            fk_superior_id=None,
            status=status,
        )

        database.session.add(membro_oficial)
        database.session.commit()
        return membro_oficial

    return _criar_membro_oficial


@pytest.fixture
def seed_membros_oficial_marechal_status_dinamico(
    seed_cargo_oficial_marechal, seed_registrar_membro
):
    def _criar_membro_oficial(status: str):
        membro = seed_registrar_membro(status=True)[1]

        membro_oficial = MembroOficialFactory(
            fk_membro_id=membro.id,
            fk_cargo_oficial_id=seed_cargo_oficial_marechal.id,
            fk_superior_id=None,
            status=status,
        )

        database.session.add(membro_oficial)
        database.session.commit()
        return membro_oficial

    return _criar_membro_oficial


@pytest.fixture
def seed_membros_oficial_general_com_superior(
    seed_registrar_membro,
    seed_cargo_oficial_general,
    seed_membros_oficial_marechal_status_dinamico,
):
    membro = seed_registrar_membro(status=True)[1]
    membro_2 = seed_registrar_membro(status=True)[1]

    marechal = seed_membros_oficial_marechal_status_dinamico(status='aprovado')

    general = MembroOficialFactory(
        fk_membro_id=membro.id,
        fk_cargo_oficial_id=seed_cargo_oficial_general.id,
        fk_superior_id=marechal.fk_membro_id,
        status='aprovado',
    )

    general_2 = MembroOficialFactory(
        fk_membro_id=membro_2.id,
        fk_cargo_oficial_id=seed_cargo_oficial_general.id,
        fk_superior_id=marechal.fk_membro_id,
        status='aprovado',
    )

    database.session.add(general)
    database.session.add(general_2)
    database.session.commit()

    return marechal


@pytest.fixture
def seed_leads_por_origem():
    leads = []
    for _ in range(4):
        lead_acutis = LeadFactory(status=True)
        lead_acutis.senha = '#Teste;@123'
        lead_acutis.origem_cadastro = OrigemCadastroEnum.acutis

        database.session.add(lead_acutis)
        leads.append(lead_acutis)

    for _ in range(4):
        lead_app = LeadFactory(status=True)
        lead_app.senha = '#Teste;@123'
        lead_app.origem_cadastro = OrigemCadastroEnum.app

        database.session.add(lead_app)
        leads.append(lead_app)

    for _ in range(4):
        lead_google = LeadFactory(status=True)
        lead_google.pais = 'pais_especifico'
        lead_google.senha = '#Teste;@123'
        lead_google.origem_cadastro = OrigemCadastroEnum.google

        database.session.add(lead_google)
        leads.append(lead_google)

    database.session.commit()

    return leads


@pytest.fixture
def seed_15_leads_campanhas(seed_registrar_membro):
    leads = []

    membro = seed_registrar_membro(status=True)[1]

    campanha_1 = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao,
        criado_por=membro.id,
        nome='Campanha do General',
    )

    database.session.add(campanha_1)

    campanha_2 = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao,
        criado_por=membro.id,
        nome='Campanha do Peixe',
    )

    database.session.add(campanha_2)

    campanha_3 = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao,
        criado_por=membro.id,
        nome='Campanha da Água',
    )

    database.session.add(campanha_3)

    for _ in range(5):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'

        database.session.add(lead)

        lead_campanha = LeadCampanhaFactory(
            fk_lead_id=lead.id, fk_campanha_id=campanha_1.id
        )
        database.session.add(lead_campanha)

        leads.append(lead)

    for _ in range(5):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'

        database.session.add(lead)

        membrolead_campanha = LeadCampanhaFactory(
            fk_lead_id=lead.id, fk_campanha_id=campanha_2.id
        )

        database.session.add(lead_campanha)
        leads.append(lead)

    for _ in range(5):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'

        database.session.add(lead)

        lead_campanha = LeadCampanhaFactory(
            fk_lead_id=lead.id, fk_campanha_id=campanha_3.id
        )

        database.session.add(lead_campanha)
        leads.append(lead)
        leads.append({'campanha_id': campanha_3.id})

    database.session.commit()

    return leads


@pytest.fixture
def seed_registra_15_membros_idade():
    membros = []
    for _ in range(5):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'
        database.session.add(lead)

        endereco = EnderecoFactory()
        database.session.add(endereco)

        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
            data_nascimento='2004-01-01',
            sexo=SexoEnum.masculino,
        )
        database.session.add(membro)
        membros.append(membro)

    for _ in range(5):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'
        database.session.add(lead)

        endereco = EnderecoFactory()
        database.session.add(endereco)

        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
            data_nascimento='1995-01-01',
            sexo=SexoEnum.feminino,
        )
        database.session.add(membro)
        membros.append(membro)

    for _ in range(5):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'
        database.session.add(lead)

        endereco = EnderecoFactory()
        database.session.add(endereco)

        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
            data_nascimento='1975-01-01',
            sexo=SexoEnum.masculino,
        )
        database.session.add(membro)
        membros.append(membro)

    database.session.commit()

    return membros


# Ágape
@pytest.fixture
def seed_nome_acao_agape():
    nome_acao_agape = NomeAcaoAgapeFactory()

    database.session.add(nome_acao_agape)

    database.session.commit()

    return nome_acao_agape


@pytest.fixture
def seed_ciclo_acao_agape():
    endereco = EnderecoFactory()
    database.session.add(endereco)

    nome_acao_agape = NomeAcaoAgapeFactory()
    database.session.add(nome_acao_agape)

    ciclo_acao_agape = CicloAcaoAgapeFactory(
        fk_endereco_id=endereco.id,
        fk_acao_agape_id=nome_acao_agape.id,
    )

    database.session.add(ciclo_acao_agape)

    database.session.commit()

    return ciclo_acao_agape


@pytest.fixture
def seed_ciclo_acao_agape_em_andamento():
    endereco = EnderecoFactory()
    database.session.add(endereco)

    nome_acao_agape = NomeAcaoAgapeFactory()
    database.session.add(nome_acao_agape)

    ciclo_acao_agape = CicloAcaoAgapeFactory(
        fk_endereco_id=endereco.id,
        fk_acao_agape_id=nome_acao_agape.id,
        status=StatusAcaoAgapeEnum.em_andamento,
    )

    database.session.add(ciclo_acao_agape)

    database.session.commit()

    return ciclo_acao_agape


@pytest.fixture
def seed_item_estoque_agape():
    item_estoque = EstoqueAgapeFactory()
    database.session.add(item_estoque)

    database.session.commit()

    return item_estoque


@pytest.fixture
def seed_registra_5_membros_campanha(seed_registrar_membro):
    membro_campanha = seed_registrar_membro(status=True)[1]
    membros = []

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao,
        criado_por=membro_campanha.id,
        nome='Campanha Viagem a Lá',
    )

    database.session.add(campanha)
    database.session.commit()

    for _ in range(5):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'
        database.session.add(lead)

        endereco = EnderecoFactory()
        database.session.add(endereco)

        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
        )
        database.session.add(membro)

        lead_campanha = LeadCampanhaFactory(
            fk_lead_id=lead.id, fk_campanha_id=campanha.id
        )

        database.session.add(lead_campanha)
        membros.append(membro)

    membros[0].criado_em = datetime(2025, 1, 8, 19, 23, 13, 390000)
    membros[1].criado_em = datetime(2025, 1, 8, 19, 23, 13, 390000)
    database.session.commit()

    return membros, campanha


@pytest.fixture
def seed_dados_doacao():
    def _dados_doacao(  # noqa: PLR0913
        *,
        campanha: Campanha,
        doacao_ativa: bool = True,
        doacao_recorrente: bool = True,
        status_doacao: StatusProcessamentoEnum = StatusProcessamentoEnum.pago,
        criado_em: datetime = None,
        numero_documento: str = None,
        anonimo: bool = False,
    ) -> tuple[Lead, Doacao]:
        endereco = EnderecoFactory()
        database.session.add(endereco)
        lead = LeadFactory(status=True)
        lead.senha = '@Teste;1234'
        database.session.add(lead)
        benfeitor = BenfeitorFactory(
            nome='Yan da Pororoca', numero_documento='14069725334'
        )
        if numero_documento:
            benfeitor.numero_documento = numero_documento
        database.session.add(benfeitor)
        membro = MembroFactory(
            fk_lead_id=lead.id,
            fk_endereco_id=endereco.id,
            fk_benfeitor_id=benfeitor.id,
        )
        database.session.add(membro)
        doacao = DoacaoFactory(
            fk_benfeitor_id=benfeitor.id,
            fk_campanha_doacao_id=campanha.campanha_doacao.id,
        )
        database.session.add(doacao)
        pagamento_doacao = PagamentoDoacaoFactory(
            fk_doacao_id=doacao.id,
            codigo_ordem_pagamento=str(uuid.uuid4()),
            recorrente=doacao_recorrente,
            ativo=doacao_ativa,
            anonimo=anonimo,
        )

        if criado_em:
            pagamento_doacao.criado_em = criado_em
        database.session.add(pagamento_doacao)

        processamento_doacao = ProcessamentoDoacaoFactory(
            fk_pagamento_doacao_id=pagamento_doacao.id,
            codigo_referencia=str(uuid.uuid4()),
            status=status_doacao,
        )
        database.session.add(processamento_doacao)
        database.session.commit()

        return lead, doacao

    return _dados_doacao


@pytest.fixture
def seed_campanha_objetivo_dinamico(seed_registrar_membro):
    def _campanha_objetivo_dinamico(
        objetivo_campanha: ObjetivosCampanhaEnum,
    ):
        membro = seed_registrar_membro(status=True)[1]

        campanha = CampanhaFactory(
            objetivo=ObjetivosCampanhaEnum.cadastro,
            criado_por=membro.id,
        )

        if objetivo_campanha:
            campanha.objetivo = objetivo_campanha
        database.session.add(campanha)
        database.session.commit()

        return campanha

    return _campanha_objetivo_dinamico


@pytest.fixture
def seed_vincula_na_campanha_verifica_periodo():
    def _vincula_na_campanha_verifica_periodo(
        campanha: Campanha,
        periodo: PeriodicidadePainelCampanhasEnum,
    ):
        for i in range(5):
            lead = LeadFactory(status=True)
            lead.senha = '#Teste;@123'
            database.session.add(lead)

            lead_campanha = LeadCampanhaFactory(
                fk_lead_id=lead.id, fk_campanha_id=campanha.id
            )
            database.session.add(lead_campanha)

            if i == 0:
                if periodo == PeriodicidadePainelCampanhasEnum.diario:
                    lead_campanha.criado_em = datetime.now() - timedelta(
                        days=1
                    )

                elif periodo == PeriodicidadePainelCampanhasEnum.semanal:
                    lead_campanha.criado_em = datetime.now() - timedelta(
                        weeks=1
                    )

                elif periodo == PeriodicidadePainelCampanhasEnum.mensal:
                    data_atual = datetime.now()
                    ano = data_atual.year
                    mes = data_atual.month - 1
                    if mes == 0:
                        mes = 12
                        ano -= 1

                    dia = data_atual.day
                    data_valida = buscar_data_valida(dia, mes, ano)
                    lead_campanha.criado_em = datetime.combine(
                        data_valida, data_atual.time()
                    )

            if campanha.objetivo == ObjetivosCampanhaEnum.cadastro:
                endereco = EnderecoFactory()
                database.session.add(endereco)
                membro = MembroFactory(
                    fk_lead_id=lead.id, fk_endereco_id=endereco.id
                )
                database.session.add(membro)

            if campanha.objetivo == ObjetivosCampanhaEnum.oficiais:
                endereco = EnderecoFactory()
                database.session.add(endereco)
                membro = MembroFactory(
                    fk_lead_id=lead.id, fk_endereco_id=endereco.id
                )
                database.session.add(membro)
                database.session.commit()

                cargo_oficial = CargosOficiaisFactory(
                    criado_por=membro.id,
                    fk_cargo_superior_id=None,
                )

                database.session.add(cargo_oficial)
                membro_oficial = MembroOficialFactory(
                    fk_membro_id=membro.id,
                    fk_superior_id=None,
                    fk_cargo_oficial_id=cargo_oficial.id,
                )
                database.session.add(membro_oficial)

        database.session.commit()

    return _vincula_na_campanha_verifica_periodo


@pytest.fixture
def seed_campanha_cadastro_sem_landingpage(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro, criado_por=membro.id
    )
    database.session.add(campanha_cadastro)

    campo_adicional_1 = CampoAdicionalFactory(
        fk_campanha_id=campanha_cadastro.id,
        tipo_campo=TiposCampoEnum.string,
        nome_campo='Nome Completo',
        obrigatorio=True,
    )
    database.session.add(campo_adicional_1)

    campo_adicional_2 = CampoAdicionalFactory(
        fk_campanha_id=campanha_cadastro.id,
        tipo_campo=TiposCampoEnum.string,
        nome_campo='Email',
        obrigatorio=True,
    )
    database.session.add(campo_adicional_2)

    database.session.commit()

    return campanha_cadastro


@pytest.fixture
def seed_landingpage_campanha(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    campanha_cadastro = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro, criado_por=membro.id
    )
    database.session.add(campanha_cadastro)

    landing_page = LandingPageFactory(fk_campanha_id=campanha_cadastro.id)
    database.session.add(landing_page)

    database.session.commit()
    return landing_page


@pytest.fixture
def seed_membro_com_todas_relacoes(seed_registrar_membro):
    lead, membro, endereco = seed_registrar_membro(status=True)

    membro_campanha = seed_registrar_membro(status=True)[1]

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao,
        criado_por=membro_campanha.id,
        nome='Campanha Viagem a Lá',
    )

    database.session.add(campanha)

    database.session.flush()

    lead_campanha = LeadCampanhaFactory(
        fk_lead_id=lead.id, fk_campanha_id=campanha.id
    )
    database.session.add(lead_campanha)

    campo_adicional_1 = CampoAdicionalFactory(
        fk_campanha_id=campanha.id,
        tipo_campo=TiposCampoEnum.string,
        nome_campo='Nome Completo',
        obrigatorio=True,
    )
    database.session.add(campo_adicional_1)
    database.session.flush()

    meta_data_lead = MetadadoLeadFactory(
        fk_lead_id=lead.id,
        fk_campo_adicional_id=campo_adicional_1.id,
        valor_campo='Valor 1',
    )
    database.session.add(meta_data_lead)
    database.session.flush()

    database.session.commit()

    return {
        'lead': lead,
        'membro': membro,
        'endereco': endereco,
        'lead_campanha': lead_campanha,
        'meta_data_lead': meta_data_lead,
    }


@pytest.fixture
def seed_registrar_live_avulsa(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao, criado_por=membro.id
    )
    database.session.add(campanha)

    live = LiveFactory(
        tag='live-avulsa-teste',
        fk_campanha_id=campanha.id,
        rede_social='youtube',
        criado_por=membro.id,
    )
    database.session.add(live)
    database.session.flush()

    live_avulsa = LiveAvulsaFactory(
        fk_livemembro_id=live.id,
        data_hora_inicio=datetime.now() + timedelta(hours=1),
        criado_por=membro.id,
    )
    database.session.add(live_avulsa)

    database.session.commit()
    return live, live_avulsa


@pytest.fixture
def seed_registrar_live_recorrente(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao, criado_por=membro.id
    )
    database.session.add(campanha)

    live = LiveFactory(
        tag='live-recorrente-teste',
        fk_campanha_id=campanha.id,
        rede_social='youtube',
        criado_por=membro.id,
    )
    database.session.add(live)
    database.session.flush()

    live_recorrente = LiveRecorrenteFactory(
        fk_live_id=live.id,
        hora_inicio=datetime.now(),
        dia_semana='quarta',
        criado_por=membro.id,
    )
    database.session.add(live_recorrente)

    database.session.commit()
    return live, live_recorrente


@pytest.fixture
def seed_registrar_canal(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao, criado_por=membro.id
    )
    database.session.add(campanha)

    live = LiveFactory(
        tag='live-teste',
        fk_campanha_id=campanha.id,
        rede_social='youtube',
        criado_por=membro.id,
    )
    database.session.add(live)
    database.session.flush()
    database.session.commit()

    return live


@pytest.fixture
def seed_audiencia_lives():
    lead = LeadFactory(status=True)
    lead.senha = '#Teste;@123'
    database.session.add(lead)

    endereco = EnderecoFactory()
    database.session.add(endereco)

    membro = MembroFactory(
        fk_lead_id=lead.id,
        fk_endereco_id=endereco.id,
    )
    database.session.add(membro)

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao,
        criado_por=membro.id,
    )
    database.session.add(campanha)

    live = LiveFactory(
        tag='live-teste',
        rede_social='youtube',
        fk_campanha_id=campanha.id,
        criado_por=membro.id,
    )

    database.session.add(live)
    database.session.flush()

    audiencia = AudienciaFactory(
        fk_live_id=live.id,
        audiencia=123,
        data_hora_registro=datetime.now(),
    )

    database.session.add(audiencia)
    database.session.commit()

    return audiencia, live


@pytest.fixture
def seed_gerar_cadastros_campanha_em_periodos(seed_registrar_membro):
    membro = seed_registrar_membro(status=True)[1]

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.cadastro,
        nome="Campanha teste",
        criado_por=membro.id
    )
    database.session.add(campanha)
    database.session.commit()

    agora = datetime.now()

    def criar_lead_campanha_com_data(data_criacao):
        lead = LeadFactory(status=True)
        lead.senha = '#Teste;@123'
        database.session.add(lead)

        lead_campanha = LeadCampanhaFactory(
            fk_lead_id=lead.id,
            fk_campanha_id=campanha.id,
        )
        lead_campanha.criado_em = data_criacao
        database.session.add(lead_campanha)

    criar_lead_campanha_com_data(agora - timedelta(hours=1))
    criar_lead_campanha_com_data(agora - timedelta(hours=23))

    criar_lead_campanha_com_data(agora - timedelta(days=2))
    criar_lead_campanha_com_data(agora - timedelta(days=6))

    criar_lead_campanha_com_data(agora - timedelta(days=10))
    criar_lead_campanha_com_data(agora - timedelta(days=29))

    database.session.commit()
    return campanha.id

@pytest.fixture
def seed_lead_voluntario_e_token(client: FlaskClient):
    lead = LeadFactory(status=True)
    database.session.add(lead)
    database.session.commit()

    perfil_voluntario = (
        database.session.query(Perfil)
        .filter_by(nome='Voluntario Agape')
        .first()
    )

    if not perfil_voluntario:
        perfil_voluntario = PerfilFactory(nome='Voluntario Agape')
        database.session.add(perfil_voluntario)
        database.session.commit()

    permissao = PermissaoLeadFactory(
        lead_id=lead.id, 
        lead=lead,
        perfil_id=perfil_voluntario.id,
        perfil=perfil_voluntario,
    )

    database.session.add(permissao)
    database.session.commit()
    database.session.flush

    payload = {'email': lead.email, 'senha': '#Teste;@123'}
    response = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = response.get_json()['access_token']

    return lead, token