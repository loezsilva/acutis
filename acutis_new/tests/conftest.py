import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import event
from testcontainers.mssql import SqlServerContainer

from acutis_api.api.app import create_app
from acutis_api.application.utils.funcoes_auxiliares import (
    buscar_data_valida,
    normalizar_texto,
)
from acutis_api.communication.enums.campanhas import (
    PeriodicidadePainelCampanhasEnum,
)
from acutis_api.communication.enums.membros import (
    OrigemCadastroEnum,
    PerfilEnum,
    SexoEnum,
)
from acutis_api.domain.entities.campanha import Campanha, ObjetivosCampanhaEnum
from acutis_api.domain.entities.campo_adicional import TiposCampoEnum
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.historico_movimentacao_agape import (
    HistoricoOrigemEnum,
    TipoMovimentacaoEnum,
)
from acutis_api.domain.entities.instancia_acao_agape import StatusAcaoAgapeEnum
from acutis_api.domain.entities.lead import Lead
from acutis_api.domain.entities.perfil import Perfil
from acutis_api.domain.entities.processamento_doacao import (
    StatusProcessamentoEnum,
)
from acutis_api.infrastructure.extensions import database
from acutis_api.infrastructure.settings import TestingConfig
from tests.factories import (
    AquisicaoAgapeFactory,
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
    CoordenadaFactory,
    DoacaoAgapeFactory,
    DoacaoFactory,
    EnderecoFactory,
    EstoqueAgapeFactory,
    FamiliaAgapeFactory,
    HistoricoMovimentacaoAgapeFactory,
    ItemDoacaoAgapeFactory,
    ItemInstanciaAgapeFactory,
    LandingPageFactory,
    LeadCampanhaFactory,
    LeadFactory,
    LiveAvulsaFactory,
    LiveFactory,
    LiveRecorrenteFactory,
    MembroAgapeFactory,
    MembroFactory,
    MembroOficialFactory,
    MenuSistemaFactory,
    MetadadoLeadFactory,
    NomeAcaoAgapeFactory,
    PagamentoDoacaoFactory,
    PerfilFactory,
    PermissaoLeadFactory,
    PermissaoMenuFactory,
    ProcessamentoDoacaoFactory,
)


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

        lead_campanha = LeadCampanhaFactory(
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
    def membro_com_todas_relacoes(  # noqa: PLR0914
        todos_campos_adicionais: bool = False,
    ):
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

        if todos_campos_adicionais:
            meta_data_lead_2 = MetadadoLeadFactory(
                fk_lead_id=lead.id,
                fk_campo_adicional_id=campo_adicional_1.id,
                valor_campo='Valor 2',
            )
            database.session.add(meta_data_lead_2)
            database.session.flush()

            campo_adicional_2 = CampoAdicionalFactory(
                fk_campanha_id=campanha.id,
                tipo_campo=TiposCampoEnum.integer,
                nome_campo='quantidade_filhos',
                obrigatorio=True,
            )
            database.session.add(campo_adicional_2)
            database.session.flush()

            meta_data_lead_3 = MetadadoLeadFactory(
                fk_lead_id=lead.id,
                fk_campo_adicional_id=campo_adicional_2.id,
                valor_campo='2',
            )
            database.session.add(meta_data_lead_3)

            campo_adicional_3 = CampoAdicionalFactory(
                fk_campanha_id=campanha.id,
                tipo_campo=TiposCampoEnum.float,
                nome_campo='altura',
                obrigatorio=True,
            )
            database.session.add(campo_adicional_3)
            database.session.flush()

            meta_data_lead_4 = MetadadoLeadFactory(
                fk_lead_id=lead.id,
                fk_campo_adicional_id=campo_adicional_3.id,
                valor_campo='1.80',
            )
            database.session.add(meta_data_lead_4)

            campo_adicional_4 = CampoAdicionalFactory(
                fk_campanha_id=campanha.id,
                tipo_campo=TiposCampoEnum.date,
                nome_campo='data_casamento',
                obrigatorio=True,
            )
            database.session.add(campo_adicional_4)
            database.session.flush()

            meta_data_lead_5 = MetadadoLeadFactory(
                fk_lead_id=lead.id,
                fk_campo_adicional_id=campo_adicional_4.id,
                valor_campo='2020-01-01',
            )
            database.session.add(meta_data_lead_5)

            campo_adicional_5 = CampoAdicionalFactory(
                fk_campanha_id=campanha.id,
                tipo_campo=TiposCampoEnum.arquivo,
                nome_campo='foto_perfil',
                obrigatorio=True,
            )
            database.session.add(campo_adicional_5)
            database.session.flush()

            meta_data_lead_6 = MetadadoLeadFactory(
                fk_lead_id=lead.id,
                fk_campo_adicional_id=campo_adicional_5.id,
                valor_campo='data:image/jpeg;base64',
            )

            database.session.add(meta_data_lead_6)

        database.session.commit()

        return {
            'lead': lead,
            'membro': membro,
            'endereco': endereco,
            'lead_campanha': lead_campanha,
            'meta_data_lead': meta_data_lead,
        }

    return membro_com_todas_relacoes


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
        fk_live_id=live.id,
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
        nome='Campanha teste',
        criado_por=membro.id,
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
def seed_membro_oficial_campos_adicionais(
    seed_registrar_membro, seed_membro_com_todas_relacoes, seed_cargo_oficial
):
    superior = seed_registrar_membro(status=True)[1]
    seed_membro_com_todas_relacoes = seed_membro_com_todas_relacoes(
        todos_campos_adicionais=True,
    )

    membro_oficial = MembroOficialFactory(
        fk_membro_id=seed_membro_com_todas_relacoes['membro'].id,
        fk_superior_id=superior.id,
        fk_cargo_oficial_id=seed_cargo_oficial.id,
    )

    database.session.add(membro_oficial)
    database.session.commit()

    return membro_oficial


@pytest.fixture
def seed_membro_com_doacao_e_campanha():
    lead = LeadFactory(status=True)
    lead.senha = '#Teste;@123'
    database.session.add(lead)

    endereco = EnderecoFactory()
    database.session.add(endereco)

    benfeitor = BenfeitorFactory()
    database.session.add(benfeitor)

    membro = MembroFactory(
        fk_lead_id=lead.id,
        fk_endereco_id=endereco.id,
        fk_benfeitor_id=benfeitor.id,
    )
    database.session.add(membro)

    campanha = CampanhaFactory(
        objetivo=ObjetivosCampanhaEnum.doacao,
        criado_por=membro.id,
    )
    database.session.add(campanha)
    database.session.flush()

    campanha_doacao = CampanhaDoacaoFactory(fk_campanha_id=campanha.id)
    database.session.add(campanha_doacao)

    lead_campanha = LeadCampanhaFactory(
        fk_lead_id=lead.id, fk_campanha_id=campanha.id
    )
    database.session.add(lead_campanha)

    doacao = DoacaoFactory(
        fk_benfeitor_id=benfeitor.id,
        fk_campanha_doacao_id=campanha_doacao.id,
    )
    database.session.add(doacao)

    pagamento_doacao = PagamentoDoacaoFactory(fk_doacao_id=doacao.id)
    database.session.add(pagamento_doacao)

    processamento_doacao = ProcessamentoDoacaoFactory(
        fk_pagamento_doacao_id=pagamento_doacao.id
    )
    database.session.add(processamento_doacao)
    database.session.commit()

    return benfeitor, membro, campanha, doacao


# Ágape
@pytest.fixture
def seed_nome_acao_agape():
    nome_acao_agape = NomeAcaoAgapeFactory()
    nome_acao_agape.nome = normalizar_texto(nome_acao_agape.nome)

    database.session.add(nome_acao_agape)

    database.session.commit()

    return nome_acao_agape


@pytest.fixture
def seed_ciclo_acao_agape():
    endereco = EnderecoFactory()
    database.session.add(endereco)
    coordenada = CoordenadaFactory(
        fk_endereco_id=endereco.id,
    )
    database.session.add(coordenada)

    nome_acao_agape = NomeAcaoAgapeFactory()
    database.session.add(nome_acao_agape)

    ciclo_acao_agape = CicloAcaoAgapeFactory(
        fk_endereco_id=endereco.id,
        fk_acao_agape_id=nome_acao_agape.id,
    )

    database.session.add(ciclo_acao_agape)

    database.session.commit()

    return ciclo_acao_agape, endereco


@pytest.fixture
def seed_ciclo_acao_agape_com_endereco():
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

    return ciclo_acao_agape, endereco


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
def seed_perfil_voluntario(seed_lead_voluntario_e_token):
    lead_voluntario = seed_lead_voluntario_e_token[0]
    perfil_voluntario = (
        database.session.query(Perfil)
        .filter_by(nome=PerfilEnum.voluntario_agape.value)
        .one_or_none()
    )

    if not perfil_voluntario:
        perfil_voluntario = PerfilFactory(
            nome=PerfilEnum.voluntario_agape.value,
            criado_por_id=lead_voluntario.id,
        )
        database.session.add(perfil_voluntario)
        database.session.commit()

    return perfil_voluntario


@pytest.fixture
def seed_perfil_benfeitor(seed_lead_voluntario_e_token):
    lead_voluntario = seed_lead_voluntario_e_token[0]
    perfil_benfeitor = (
        database.session.query(Perfil)
        .filter_by(nome=PerfilEnum.benfeitor.value)
        .one_or_none()
    )

    if not perfil_benfeitor:
        perfil_benfeitor = PerfilFactory(
            nome=PerfilEnum.benfeitor.value,
            criado_por_id=lead_voluntario.id,
        )
        database.session.add(perfil_benfeitor)
        database.session.commit()

    return perfil_benfeitor


@pytest.fixture
def seed_menu_agape_e_permissoes(
    seed_perfil_voluntario,
    seed_lead_voluntario_e_token,
):
    lead_voluntario = seed_lead_voluntario_e_token[0]
    menu_sistema = MenuSistemaFactory(
        slug='familia_agape',
        criado_por_id=lead_voluntario.id,
    )

    database.session.add(menu_sistema)
    database.session.commit()

    permissao_menu = PermissaoMenuFactory(
        perfil_id=seed_perfil_voluntario.id,
        menu_id=menu_sistema.id,
        acessar=True,
        criar=True,
        editar=True,
        deletar=True,
    )
    database.session.add(permissao_menu)
    database.session.commit()

    return menu_sistema, permissao_menu


@pytest.fixture
def seed_lead_voluntario_e_token(client: FlaskClient):
    lead = LeadFactory(status=True)
    lead.senha = '#Teste;@123'
    database.session.add(lead)
    database.session.commit()

    perfil_voluntario = (
        database.session.query(Perfil)
        .filter_by(nome='Voluntario Agape')
        .one_or_none()
    )

    if not perfil_voluntario:
        perfil_voluntario = PerfilFactory(
            nome='Voluntario Agape',
            criado_por_id=lead.id,
        )
        database.session.add(perfil_voluntario)
        database.session.commit()

    permissao = PermissaoLeadFactory(
        lead_id=lead.id,
        perfil_id=perfil_voluntario.id,
        criado_por_id=lead.id,
    )

    database.session.add(permissao)
    database.session.commit()

    payload = {'email': lead.email, 'senha': '#Teste;@123'}
    response = client.post(
        '/api/autenticacao/login?httponly=false', json=payload
    )
    token = response.get_json()['access_token']

    database.session.flush()

    return lead, token


@pytest.fixture
def seed_familia_com_endereco(seed_membro):
    endereco_criado = EnderecoFactory()
    database.session.add(endereco_criado)
    database.session.commit()

    coordenada = CoordenadaFactory(
        fk_endereco_id=endereco_criado.id,
    )
    database.session.add(coordenada)
    database.session.commit()

    familia_criada = FamiliaAgapeFactory(
        fk_endereco_id=endereco_criado.id, cadastrada_por=seed_membro.id
    )
    database.session.add(familia_criada)
    database.session.commit()

    membro_familia = MembroAgapeFactory(
        fk_familia_agape_id=familia_criada.id,
        responsavel=True,
    )
    database.session.add(membro_familia)
    database.session.commit()

    return familia_criada, endereco_criado


@pytest.fixture
def seed_familia_com_cpf_especifico(
    seed_familia_com_endereco, seed_ciclo_acao_agape
):
    ciclo_acao = seed_ciclo_acao_agape[0]

    familia = seed_familia_com_endereco[0]

    membro_responsavel = MembroAgapeFactory(
        fk_familia_agape_id=familia.id,
        responsavel=True,
        cpf='12345678901',
    )
    database.session.add(membro_responsavel)
    database.session.commit()
    database.session.flush()

    doacao_agape = DoacaoAgapeFactory(
        fk_familia_agape_id=familia.id,
    )
    database.session.add(doacao_agape)
    database.session.commit()
    database.session.flush()

    item_estoque = EstoqueAgapeFactory()
    database.session.add(item_estoque)
    database.session.commit()
    database.session.flush()

    item_instancia_agape = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_acao.id,
        fk_estoque_agape_id=item_estoque.id,
    )
    database.session.add(item_instancia_agape)
    database.session.commit()
    database.session.flush()

    item_doacao = ItemDoacaoAgapeFactory(
        fk_item_instancia_agape_id=item_instancia_agape.id,
        fk_doacao_agape_id=doacao_agape.id,
    )

    database.session.add(item_doacao)
    database.session.commit()
    database.session.flush()

    return familia


@pytest.fixture
def seed_ciclo_acao_com_itens(seed_ciclo_acao_agape_em_andamento):
    ciclo_acao = seed_ciclo_acao_agape_em_andamento

    itens_estoque_criados = []
    items_instancia_criados = []
    for i in range(3):
        item_estoque = EstoqueAgapeFactory(item=f'Item de Teste {i + 1}')
        database.session.add(item_estoque)
        itens_estoque_criados.append(item_estoque)

    database.session.commit()

    for item_estoque in itens_estoque_criados:
        item_instancia = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=ciclo_acao.id,
            fk_estoque_agape_id=item_estoque.id,
            quantidade=5 + itens_estoque_criados.index(item_estoque),
        )
        database.session.add(item_instancia)
        items_instancia_criados.append(item_instancia)

    database.session.commit()

    return ciclo_acao, items_instancia_criados


@pytest.fixture
def seed_ciclo_acao_nao_iniciado_com_itens(seed_ciclo_acao_agape):
    ciclo_acao = seed_ciclo_acao_agape[0]

    itens_estoque_criados = []
    items_instancia_criados = []
    for i in range(3):
        item_estoque = EstoqueAgapeFactory(item=f'Item de Teste {i + 1}')
        database.session.add(item_estoque)
        itens_estoque_criados.append(item_estoque)

    database.session.commit()

    for item_estoque in itens_estoque_criados:
        item_instancia = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=ciclo_acao.id,
            fk_estoque_agape_id=item_estoque.id,
            quantidade=5 + itens_estoque_criados.index(item_estoque),
        )
        database.session.add(item_instancia)
        items_instancia_criados.append(item_instancia)

    database.session.commit()

    return ciclo_acao, items_instancia_criados


@pytest.fixture
def seed_membro():
    endereco_criado = EnderecoFactory()
    database.session.add(endereco_criado)
    database.session.commit()

    lead_cadastrou = LeadFactory(status=True)
    lead_cadastrou.senha = '#Teste;@123'
    database.session.add(lead_cadastrou)
    database.session.commit()

    membro = MembroFactory(
        fk_lead_id=lead_cadastrou.id,
        fk_endereco_id=endereco_criado.id,
    )

    database.session.add(membro)
    database.session.commit()

    return membro


@pytest.fixture
def seed_membro_agape(seed_familia_com_endereco):
    familia = seed_familia_com_endereco[0]

    membro = MembroAgapeFactory(
        fk_familia_agape_id=familia.id,
    )
    database.session.add(membro)
    database.session.commit()

    return membro


@pytest.fixture
def seed_familia_com_membros_e_rendas(seed_familia_com_endereco):
    """
    Cria uma família ágape com múltiplos membros, cada um com rendas
    variadas, e retorna a família, a renda total esperada e o número
    de membros.
    """

    familia = seed_familia_com_endereco[0]

    rendas = [Decimal('100.50'), Decimal('75.25'), Decimal('0.00'), None]
    membros_criados = []
    renda_total_calculada = Decimal('0.00')

    for i, renda_valor in enumerate(rendas):
        membro = MembroAgapeFactory(
            fk_familia_agape_id=familia.id,
            renda=(
                Decimal(str(renda_valor)) if renda_valor is not None else None
            ),
        )
        database.session.add(membro)
        membros_criados.append(membro)
        if renda_valor is not None:
            renda_total_calculada += Decimal(str(renda_valor))

    database.session.commit()

    numero_total_membros = len(membros_criados)

    return familia, renda_total_calculada, numero_total_membros


@pytest.fixture
def seed_familia_com_recebimentos(seed_familia_com_endereco):
    """
    Cria uma família com múltiplas doações e itens, e retorna a família
    junto com os totais esperados para o card de recebimentos.
    """

    familia = seed_familia_com_endereco[0]

    nome_acao = NomeAcaoAgapeFactory()
    database.session.add(nome_acao)
    endereco_ciclo = EnderecoFactory(cidade='Cidade Ciclo Doacao')
    database.session.add(endereco_ciclo)
    database.session.commit()

    ciclo_acao = CicloAcaoAgapeFactory(
        fk_acao_agape_id=nome_acao.id,
        fk_endereco_id=endereco_ciclo.id,
        status=StatusAcaoAgapeEnum.finalizado,
    )
    database.session.add(ciclo_acao)
    database.session.commit()

    # Criar alguns itens de estoque distintos
    item_estoque1 = EstoqueAgapeFactory(item='Arroz Tipo A')
    item_estoque2 = EstoqueAgapeFactory(item='Feijão Tipo B')
    item_estoque3 = EstoqueAgapeFactory(item='Óleo Tipo C')
    database.session.add_all([item_estoque1, item_estoque2, item_estoque3])
    database.session.commit()

    # Doação 1
    doacao1 = DoacaoAgapeFactory(
        fk_familia_agape_id=familia.id,
    )
    database.session.add(doacao1)
    database.session.commit()

    item_instancia_agape1 = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_acao.id,
        fk_estoque_agape_id=item_estoque1.id,
        quantidade=5,
    )
    item_instancia_agape2 = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_acao.id,
        fk_estoque_agape_id=item_estoque2.id,
        quantidade=5,
    )
    database.session.add_all([item_instancia_agape1, item_instancia_agape2])
    database.session.commit()

    item_doacao1_1 = ItemDoacaoAgapeFactory(
        fk_doacao_agape_id=doacao1.id,
        fk_item_instancia_agape_id=item_instancia_agape1.id,
        quantidade=2,
    )

    item_doacao1_2 = ItemDoacaoAgapeFactory(
        fk_doacao_agape_id=doacao1.id,
        fk_item_instancia_agape_id=item_instancia_agape2.id,
        quantidade=3,
    )
    database.session.add_all([item_doacao1_1, item_doacao1_2])
    database.session.commit()

    doacao2 = DoacaoAgapeFactory(
        fk_familia_agape_id=familia.id,
    )
    database.session.add(doacao2)
    database.session.commit()

    item_instancia_agape2_1 = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_acao.id,
        fk_estoque_agape_id=item_estoque1.id,
        quantidade=5,
    )
    item_instancia_agape2_2 = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_acao.id,
        fk_estoque_agape_id=item_estoque2.id,
        quantidade=5,
    )
    database.session.add_all([
        item_instancia_agape2_1,
        item_instancia_agape2_2,
    ])
    database.session.commit()

    database.session.add_all([
        ItemDoacaoAgapeFactory(
            fk_doacao_agape_id=doacao2.id,
            fk_item_instancia_agape_id=item_instancia_agape2_1.id,
            quantidade=1,
        ),
        ItemDoacaoAgapeFactory(
            fk_doacao_agape_id=doacao2.id,
            fk_item_instancia_agape_id=item_instancia_agape2_2.id,
            quantidade=4,
        ),
    ])
    database.session.commit()

    return (
        familia,
        2 + 3 + 1 + 4,  # = 10
    )


@pytest.fixture
def seed_varias_familias_para_estatisticas(seed_membro):
    familias_criadas_info = []

    endereco1 = EnderecoFactory()
    database.session.add(endereco1)
    database.session.commit()
    familia1 = FamiliaAgapeFactory(
        fk_endereco_id=endereco1.id,
        cadastrada_por=seed_membro.id,
    )
    database.session.add(familia1)
    database.session.commit()
    database.session.add(
        MembroAgapeFactory(fk_familia_agape_id=familia1.id),
    )
    familias_criadas_info.append((familia1, 1))

    endereco2 = EnderecoFactory()
    database.session.add(endereco2)
    database.session.commit()
    familia2 = FamiliaAgapeFactory(
        fk_endereco_id=endereco2.id,
        cadastrada_por=seed_membro.id,
    )
    database.session.add(familia2)
    database.session.commit()

    database.session.add_all([
        MembroAgapeFactory(fk_familia_agape_id=familia2.id) for _ in range(3)
    ])

    familias_criadas_info.append((familia2, 3))

    endereco3 = EnderecoFactory()
    database.session.add(endereco3)
    database.session.commit()
    familia3 = FamiliaAgapeFactory(
        fk_endereco_id=endereco3.id,
        cadastrada_por=seed_membro.id,
    )
    database.session.add(familia3)
    database.session.commit()
    database.session.add_all([
        MembroAgapeFactory(fk_familia_agape_id=familia3.id) for _ in range(5)
    ])
    familias_criadas_info.append((familia3, 5))

    endereco4 = EnderecoFactory()
    database.session.add(endereco4)
    database.session.commit()
    familia4_sem_membros = FamiliaAgapeFactory(
        fk_endereco_id=endereco4.id,
        cadastrada_por=seed_membro.id,
    )
    database.session.add(familia4_sem_membros)
    familias_criadas_info.append((familia4_sem_membros, 0))

    database.session.commit()

    total_familias = len(familias_criadas_info)
    total_membros = sum(
        num_membros for _, num_membros in familias_criadas_info
    )

    media_membros_por_familia = (
        Decimal(str(total_membros)) / Decimal(str(total_familias))
        if total_familias > 0
        else Decimal('0.0')
    )

    total_familias_com_apenas_um_membro = sum(
        1 for _, num_membros in familias_criadas_info if num_membros == 1
    )
    total_familias_com_cinco_ou_mais_membros = sum(
        1 for _, num_membros in familias_criadas_info if num_membros >= 5
    )

    return {
        'total_familias': total_familias,
        'total_membros': total_membros,
        'media_membros_por_familia': float(
            media_membros_por_familia.quantize(Decimal('0.01'))
        ),
        'total_familias_com_apenas_um_membro': (
            total_familias_com_apenas_um_membro
        ),
        'total_familias_com_cinco_ou_mais_membros': (
            total_familias_com_cinco_ou_mais_membros
        ),
    }


@pytest.fixture
def seed_ciclo_acao_agape_finalizado():
    endereco = EnderecoFactory()
    database.session.add(endereco)

    nome_acao_agape = NomeAcaoAgapeFactory()
    database.session.add(nome_acao_agape)

    ciclo_acao_agape = CicloAcaoAgapeFactory(
        fk_endereco_id=endereco.id,
        fk_acao_agape_id=nome_acao_agape.id,
        data_termino=datetime(2023, 12, 20),
        status=StatusAcaoAgapeEnum.finalizado,
    )

    database.session.add(ciclo_acao_agape)

    database.session.commit()

    return ciclo_acao_agape


@pytest.fixture
def seed_varios_itens_estoque_para_estatisticas(
    seed_ciclo_acao_agape_finalizado,
):
    """
    Cria vários itens no estoque com diferentes quantidades para testar
    o endpoint de estatísticas de itens de estoque.
    Retorna um dicionário com as estatísticas esperadas.
    """

    ciclo_acao = seed_ciclo_acao_agape_finalizado

    itens_criados_detalhes = [
        {'item': 'Arroz 1kg', 'quantidade': 20},
        {'item': 'Feijão Carioca 1kg', 'quantidade': 15},
        {'item': 'Óleo de Soja 900ml', 'quantidade': 5},
        {'item': 'Açúcar Refinado 1kg', 'quantidade': 0},
        {'item': 'Sal Refinado 1kg', 'quantidade': 3},
        {'item': 'Macarrão Espaguete 500g', 'quantidade': 30},
        {'item': 'Farinha de Trigo 1kg', 'quantidade': 0},
    ]

    for detalhe_item in itens_criados_detalhes:
        item_estoque = EstoqueAgapeFactory(**detalhe_item)
        database.session.add(item_estoque)
        database.session.flush()

        database.session.add(
            ItemInstanciaAgapeFactory(
                fk_instancia_acao_agape_id=ciclo_acao.id,
                fk_estoque_agape_id=item_estoque.id,
                quantidade=5,
            )
        )
        database.session.add(
            AquisicaoAgapeFactory(
                fk_estoque_agape_id=item_estoque.id,
                quantidade=5,
            )
        )

    database.session.commit()

    total_tipos_item = len(itens_criados_detalhes)
    quantidade_total_itens = sum(
        d['quantidade'] for d in itens_criados_detalhes
    )
    total_itens_zerados = sum(
        1 for d in itens_criados_detalhes if d['quantidade'] == 0
    )

    total_itens_baixo_estoque = sum(
        1 for d in itens_criados_detalhes if 0 < d['quantidade'] <= 5
    )

    expected_stats = {
        'total_tipos_item': total_tipos_item,
        'quantidade_total_itens': quantidade_total_itens,
        'total_itens_zerados': total_itens_zerados,
        'total_itens_baixo_estoque': total_itens_baixo_estoque,
    }

    return expected_stats


@pytest.fixture
def seed_ciclo_com_doacoes_completas(
    seed_membro,
):
    """
    Cria um ciclo de ação com famílias, membros, doações e itens
    para testar a funcionalidade de exportação.
    Retorna o ciclo_acao, e listas de familias, membros e itens doados
    para facilitar as asserções.
    """

    nome_acao = NomeAcaoAgapeFactory(nome='Ação de Natal')
    endereco_ciclo = EnderecoFactory(cidade='Fortaleza', bairro='Centro')
    database.session.add_all([nome_acao, endereco_ciclo])
    database.session.commit()

    ciclo_acao = CicloAcaoAgapeFactory(
        fk_acao_agape_id=nome_acao.id,
        fk_endereco_id=endereco_ciclo.id,
        status=StatusAcaoAgapeEnum.finalizado,
        data_inicio=datetime(2023, 12, 1),
        data_termino=datetime(2023, 12, 20),
    )
    database.session.add(ciclo_acao)
    database.session.commit()

    item_arroz = EstoqueAgapeFactory(
        item='Arroz Parboilizado 1kg', quantidade=100
    )
    item_feijao = EstoqueAgapeFactory(
        item='Feijão Carioca 1kg', quantidade=100
    )
    item_macarrao = EstoqueAgapeFactory(
        item='Macarrão Espaguete 500g', quantidade=100
    )
    database.session.add_all([item_arroz, item_feijao, item_macarrao])
    database.session.commit()

    item_instancia_arroz = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_acao.id,
        fk_estoque_agape_id=item_arroz.id,
        quantidade=50,
    )
    item_instancia_feijao = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_acao.id,
        fk_estoque_agape_id=item_feijao.id,
        quantidade=50,
    )
    item_instancia_macarrao = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_acao.id,
        fk_estoque_agape_id=item_macarrao.id,
        quantidade=30,
    )
    database.session.add_all([
        item_instancia_arroz,
        item_instancia_feijao,
        item_instancia_macarrao,
    ])
    database.session.commit()

    familias_criadas = []
    membros_responsaveis_criados = []

    doacoes_info = []

    endereco_familia1 = EnderecoFactory(
        cidade='Fortaleza', bairro='Aldeota', codigo_postal='60100001'
    )
    cadastrada_por_membro1 = seed_membro
    database.session.add(endereco_familia1)
    database.session.commit()
    familia1 = FamiliaAgapeFactory(
        fk_endereco_id=endereco_familia1.id,
        nome_familia='Família Silva',
        cadastrada_por=cadastrada_por_membro1.id,
    )
    database.session.add(familia1)
    database.session.commit()
    responsavel1 = MembroAgapeFactory(
        fk_familia_agape_id=familia1.id,
        nome='João Silva',
        cpf='11122233344',
        responsavel=True,
    )
    database.session.add(responsavel1)
    database.session.commit()
    familias_criadas.append(familia1)
    membros_responsaveis_criados.append(responsavel1)

    doacao1 = DoacaoAgapeFactory(
        fk_familia_agape_id=familia1.id,
    )
    database.session.add(doacao1)
    database.session.commit()

    item_doado1_arroz = ItemDoacaoAgapeFactory(
        fk_doacao_agape_id=doacao1.id,
        fk_item_instancia_agape_id=item_instancia_arroz.id,
        quantidade=2,
    )
    item_doado1_feijao = ItemDoacaoAgapeFactory(
        fk_doacao_agape_id=doacao1.id,
        fk_item_instancia_agape_id=item_instancia_feijao.id,
        quantidade=1,
    )
    database.session.add_all([item_doado1_arroz, item_doado1_feijao])
    database.session.commit()
    doacoes_info.append({
        'familia': familia1,
        'responsavel_cpf': responsavel1.cpf,
        'itens': [(item_arroz.item, 2), (item_feijao.item, 1)],
    })

    endereco_familia2 = EnderecoFactory(
        cidade='Fortaleza', bairro='Meireles', codigo_postal='60200002'
    )
    cadastrada_por_membro2 = seed_membro
    database.session.add(endereco_familia2)
    database.session.commit()
    familia2 = FamiliaAgapeFactory(
        fk_endereco_id=endereco_familia2.id,
        nome_familia='Família Souza',
        cadastrada_por=cadastrada_por_membro2.id,
    )
    database.session.add(familia2)
    database.session.commit()
    responsavel2 = MembroAgapeFactory(
        fk_familia_agape_id=familia2.id,
        nome='Maria Souza',
        cpf='55566677788',
        responsavel=True,
    )
    database.session.add(responsavel2)
    database.session.commit()
    familias_criadas.append(familia2)
    membros_responsaveis_criados.append(responsavel2)

    doacao2 = DoacaoAgapeFactory(
        fk_familia_agape_id=familia2.id,
    )
    database.session.add(doacao2)
    database.session.commit()

    item_doado2_macarrao = ItemDoacaoAgapeFactory(
        fk_doacao_agape_id=doacao2.id,
        fk_item_instancia_agape_id=item_instancia_macarrao.id,
        quantidade=3,
    )
    database.session.add(item_doado2_macarrao)
    database.session.commit()
    doacoes_info.append({
        'familia': familia2,
        'responsavel_cpf': responsavel2.cpf,
        'itens': [(item_macarrao.item, 3)],
    })

    return {
        'ciclo_acao': ciclo_acao,
        'nome_acao': nome_acao,
        'doacoes_info': doacoes_info,
    }


@pytest.fixture
def seed_diversas_familias_para_exportacao(
    seed_membro,
):
    """
    Cria um conjunto diversificado de famílias Ágape para testar a exportação.
    Retorna uma lista de todas as famílias criadas que devem ser exportadas.
    """
    familias_exportaveis = []
    membro_cadastrador = seed_membro

    end1 = EnderecoFactory(
        logradouro='Rua das Flores',
        numero='123',
        bairro='Jardim',
        cidade='Floral',
        estado='FL',
        codigo_postal='10000001',
    )
    database.session.add(end1)
    database.session.commit()
    fam1 = FamiliaAgapeFactory(
        nome_familia='Família Almeida',
        fk_endereco_id=end1.id,
        observacao='Nenhuma observação especial.',
        status=True,
        deletado_em=None,
        cadastrada_por=membro_cadastrador.id,
    )
    database.session.add(fam1)
    database.session.commit()
    MembroAgapeFactory(
        fk_familia_agape_id=fam1.id,
        nome='Carlos Almeida',
        responsavel=True,
        cpf='11100011101',
        telefone='11999911101',
        email='carlos@almeida.com',
    )
    MembroAgapeFactory(
        fk_familia_agape_id=fam1.id, nome='Ana Almeida', responsavel=False
    )
    familias_exportaveis.append(fam1)

    end2 = EnderecoFactory(
        logradouro='Avenida Principal',
        numero='456',
        bairro='Centro',
        cidade='Metropole',
        estado='MP',
        codigo_postal='20000002',
    )
    database.session.add(end2)
    database.session.commit()
    fam2 = FamiliaAgapeFactory(
        nome_familia='Família Costa',
        fk_endereco_id=end2.id,
        observacao=None,
        status=True,
        deletado_em=None,
        cadastrada_por=membro_cadastrador.id,
    )
    database.session.add(fam2)
    database.session.commit()
    MembroAgapeFactory(
        fk_familia_agape_id=fam2.id,
        nome='Beatriz Costa',
        responsavel=True,
        cpf='22200022202',
        telefone='22999922202',
        email='bia@costa.com',
    )
    familias_exportaveis.append(fam2)

    end3 = EnderecoFactory(
        logradouro='Travessa dos Sonhos',
        numero='78',
        bairro='Paraíso',
        cidade='Campina',
        estado='CA',
        codigo_postal='30000003',
    )
    database.session.add(end3)
    database.session.commit()
    obs_longa = (
        'Esta família necessita de acompanhamento especial devido a '
        'condições de moradia. Contato preferencial pela manhã.'
    )
    fam3 = FamiliaAgapeFactory(
        nome_familia='Família Oliveira',
        fk_endereco_id=end3.id,
        observacao=obs_longa,
        status=True,
        deletado_em=None,
        cadastrada_por=membro_cadastrador.id,
    )
    database.session.add(fam3)
    database.session.commit()
    MembroAgapeFactory(
        fk_familia_agape_id=fam3.id,
        nome='Daniel Oliveira',
        responsavel=True,
        cpf='33300033303',
        telefone='33999933303',
        email='daniel@oliveira.com',
    )
    MembroAgapeFactory(
        fk_familia_agape_id=fam3.id, nome='Elisa Oliveira', responsavel=False
    )
    MembroAgapeFactory(
        fk_familia_agape_id=fam3.id,
        nome='Fernando Oliveira',
        responsavel=False,
    )
    familias_exportaveis.append(fam3)

    end4 = EnderecoFactory(
        logradouro='Rua Esquecida',
        numero='0',
        bairro='Limbo',
        cidade='Perdida',
        estado='LP',
        codigo_postal='40000004',
    )
    database.session.add(end4)
    database.session.commit()
    fam4_deletada = FamiliaAgapeFactory(
        nome_familia='Família Fantasma',
        fk_endereco_id=end4.id,
        status=False,
        deletado_em=datetime.now(),
        cadastrada_por=membro_cadastrador.id,
    )
    database.session.add(fam4_deletada)
    database.session.commit()
    MembroAgapeFactory(
        fk_familia_agape_id=fam4_deletada.id,
        nome='Sr. Sumido',
        responsavel=True,
        cpf='44400044404',
    )

    database.session.flush()

    return familias_exportaveis


@pytest.fixture
def seed_historico_movimentacoes_agape(
    seed_item_estoque_agape,
    seed_ciclo_acao_com_itens,
    seed_familia_com_endereco,
):
    """
    Popula o banco de dados com dados de histórico de movimentações do ágape.
    Cria movimentações de entrada (abastecimento) e saída (doação).
    Retorna uma lista dos objetos HistoricoMovimentacaoAgape criados.
    """

    historicos_criados = []

    ciclo_acao, itens_instancia_ciclo = seed_ciclo_acao_com_itens
    familia_beneficiada, _ = seed_familia_com_endereco

    item_estoque_existente = seed_item_estoque_agape
    historico_entrada = HistoricoMovimentacaoAgapeFactory(
        fk_estoque_agape_id=item_estoque_existente.id,
        tipo_movimentacoes=TipoMovimentacaoEnum.entrada,
        quantidade=50,
        origem=HistoricoOrigemEnum.estoque,
        destino=HistoricoOrigemEnum.estoque,
    )
    historico_entrada.fk_instancia_acao_agape_id = ciclo_acao.id
    database.session.add(historico_entrada)
    historicos_criados.append(historico_entrada)

    if not itens_instancia_ciclo:
        raise ValueError(
            'A fixture seed_ciclo_acao_com_itens não retornou itens_instancia.'
        )

    item_instancia_para_doar = itens_instancia_ciclo[0]

    doacao = DoacaoAgapeFactory(
        fk_familia_agape_id=familia_beneficiada.id,
    )
    database.session.add(doacao)
    database.session.flush()

    item_doacao = ItemDoacaoAgapeFactory(
        fk_doacao_agape_id=doacao.id,
        fk_item_instancia_agape_id=item_instancia_para_doar.id,
        quantidade=5,
    )
    database.session.add(item_doacao)
    database.session.flush()

    historico_saida = HistoricoMovimentacaoAgapeFactory(
        fk_estoque_agape_id=item_instancia_para_doar.fk_estoque_agape_id,
        tipo_movimentacoes=TipoMovimentacaoEnum.saida,
        quantidade=50,
        origem=HistoricoOrigemEnum.estoque,
        destino=HistoricoOrigemEnum.estoque,
    )
    historico_saida.fk_instancia_acao_agape_id = ciclo_acao.id
    database.session.add(historico_saida)
    historicos_criados.append(historico_saida)

    historico_entrada_2 = HistoricoMovimentacaoAgapeFactory(
        fk_estoque_agape_id=item_estoque_existente.id,
        tipo_movimentacoes=TipoMovimentacaoEnum.saida,
        quantidade=50,
        origem=HistoricoOrigemEnum.estoque,
        destino=HistoricoOrigemEnum.estoque,
    )
    historico_entrada_2.fk_instancia_acao_agape_id = ciclo_acao.id
    database.session.add(historico_entrada_2)
    historicos_criados.append(historico_entrada_2)

    if len(itens_instancia_ciclo) > 1:
        item_instancia_para_doar_2 = itens_instancia_ciclo[1]

        doacao_2 = DoacaoAgapeFactory(
            fk_familia_agape_id=familia_beneficiada.id,
        )
        database.session.add(doacao_2)
        database.session.flush()

        item_doacao_2 = ItemDoacaoAgapeFactory(
            fk_doacao_agape_id=doacao_2.id,
            fk_item_instancia_agape_id=item_instancia_para_doar_2.id,
            quantidade=3,
        )
        database.session.add(item_doacao_2)
        database.session.flush()

        historico_saida_2 = HistoricoMovimentacaoAgapeFactory(
            fk_estoque_agape_id=item_instancia_para_doar_2.fk_estoque_agape_id,
            tipo_movimentacoes=TipoMovimentacaoEnum.saida,
            quantidade=50,
            origem=HistoricoOrigemEnum.estoque,
            destino=HistoricoOrigemEnum.estoque,
        )
        historico_saida_2.fk_instancia_acao_agape_id = ciclo_acao.id
        database.session.add(historico_saida_2)
        historicos_criados.append(historico_saida_2)

    database.session.commit()

    historicos_criados.sort(key=lambda x: x.criado_em, reverse=True)

    return historicos_criados


@pytest.fixture
def seed_geolocalizacoes_beneficiarios_ciclo_acao(
    seed_nome_acao_agape,
    seed_membro,
):
    endereco_ciclo = EnderecoFactory()
    database.session.add(endereco_ciclo)
    database.session.commit()

    ciclo_acao_principal = CicloAcaoAgapeFactory(
        fk_acao_agape_id=seed_nome_acao_agape.id,
        fk_endereco_id=endereco_ciclo.id,
    )
    database.session.add(ciclo_acao_principal)
    database.session.commit()

    geolocalizacoes_esperadas = []

    for i in range(3):
        endereco_familia = EnderecoFactory()
        coordenada_familia = CoordenadaFactory(
            fk_endereco_id=endereco_familia.id
        )
        database.session.add(endereco_familia)
        database.session.add(coordenada_familia)
        database.session.commit()

        familia = FamiliaAgapeFactory(
            fk_endereco_id=endereco_familia.id, cadastrada_por=seed_membro.id
        )
        database.session.add(familia)
        database.session.commit()

        responsavel = MembroAgapeFactory(
            fk_familia_agape_id=familia.id,
            nome=f'Responsável Família {i + 1}',
            responsavel=True,
        )
        database.session.add(responsavel)
        database.session.commit()

        doacao = DoacaoAgapeFactory(
            fk_familia_agape_id=familia.id,
        )
        database.session.add(doacao)
        database.session.commit()

        item_estoque_ciclo = EstoqueAgapeFactory()
        database.session.add(item_estoque_ciclo)
        database.session.commit()

        item_instancia_ciclo = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=ciclo_acao_principal.id,
            fk_estoque_agape_id=item_estoque_ciclo.id,
            quantidade=10,
        )
        database.session.add(item_instancia_ciclo)
        database.session.commit()

        item_doacao = ItemDoacaoAgapeFactory(
            fk_doacao_agape_id=doacao.id,
            fk_item_instancia_agape_id=item_instancia_ciclo.id,
            quantidade=1,
        )
        database.session.add(item_doacao)

        geolocalizacoes_esperadas.append({
            'latitude': coordenada_familia.latitude,
            'longitude': coordenada_familia.longitude,
            'nome_familia': familia.nome_familia,
        })

    geolocalizacoes_esperadas.sort(key=lambda g: g['nome_familia'])

    return ciclo_acao_principal.id, geolocalizacoes_esperadas


@pytest.fixture
def seed_doacao_com_itens_doados(
    seed_familia_com_endereco,
    seed_ciclo_acao_agape,
):
    familia, _ = seed_familia_com_endereco
    ciclo_acao, _ = seed_ciclo_acao_agape

    itens_esperados = []

    doacao = DoacaoAgapeFactory(
        fk_familia_agape_id=familia.id,
    )
    database.session.add(doacao)
    database.session.flush()

    for i in range(2):
        item_estoque = EstoqueAgapeFactory(
            item=f'Item Teste Doado {i + 1}', quantidade=100
        )
        database.session.add(item_estoque)
        database.session.flush()

        item_instancia = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=ciclo_acao.id,
            fk_estoque_agape_id=item_estoque.id,
            quantidade=20,
        )
        database.session.add(item_instancia)
        database.session.flush()

        quantidade_doada_neste_item = 5 + i
        item_doado = ItemDoacaoAgapeFactory(
            fk_doacao_agape_id=doacao.id,
            fk_item_instancia_agape_id=item_instancia.id,
            quantidade=quantidade_doada_neste_item,
        )
        database.session.add(item_doado)
        database.session.flush()

        itens_esperados.append({
            'item_id': item_estoque.id,
            'nome_item': item_estoque.item,
            'quantidade_doada': quantidade_doada_neste_item,
            'item_doacao_agape_id': item_doado.id,
            'item_instancia_agape_id': item_instancia.id,
        })

    database.session.commit()

    itens_esperados.sort(key=lambda x: x['nome_item'])

    return doacao.id, itens_esperados


@pytest.fixture
def seed_doacao_sem_itens(
    seed_familia_com_endereco,
):
    from tests.factories import DoacaoAgapeFactory

    familia, _ = seed_familia_com_endereco

    doacao = DoacaoAgapeFactory(
        fk_familia_agape_id=familia.id,
    )
    database.session.add(doacao)
    database.session.commit()

    return doacao.id


@pytest.fixture
def seed_itens_recebidos_em_ciclo_doacao(
    seed_familia_com_endereco,
    seed_nome_acao_agape,
):
    familia, _ = seed_familia_com_endereco

    endereco_ciclo_principal = EnderecoFactory()
    database.session.add(endereco_ciclo_principal)
    database.session.flush()

    nome_acao_principal = seed_nome_acao_agape
    ciclo_principal = CicloAcaoAgapeFactory(
        fk_acao_agape_id=nome_acao_principal.id,
        fk_endereco_id=endereco_ciclo_principal.id,
    )
    database.session.add(ciclo_principal)
    database.session.flush()

    doacao_principal = DoacaoAgapeFactory(fk_familia_agape_id=familia.id)
    database.session.add(doacao_principal)
    database.session.flush()

    itens_esperados_principal = []
    for i in range(2):
        item_estoque = EstoqueAgapeFactory(item=f'Item Principal {i + 1}')
        database.session.add(item_estoque)
        database.session.flush()

        item_instancia = ItemInstanciaAgapeFactory(
            fk_instancia_acao_agape_id=ciclo_principal.id,
            fk_estoque_agape_id=item_estoque.id,
            quantidade=30,
        )
        database.session.add(item_instancia)
        database.session.flush()

        quantidade_doada = 10 + i
        item_doado = ItemDoacaoAgapeFactory(
            fk_doacao_agape_id=doacao_principal.id,
            fk_item_instancia_agape_id=item_instancia.id,
            quantidade=quantidade_doada,
        )
        database.session.add(item_doado)
        database.session.flush()
        itens_esperados_principal.append({
            'item_id': item_estoque.id,
            'nome_item': item_estoque.item,
            'quantidade_doada': quantidade_doada,
            'item_doacao_agape_id': item_doado.id,
            'item_instancia_agape_id': item_instancia.id,
        })

    endereco_ciclo_secundario = EnderecoFactory(cidade='Outra Cidade')
    database.session.add(endereco_ciclo_secundario)
    database.session.flush()

    nome_acao_secundaria = NomeAcaoAgapeFactory(nome='Ação Secundária')
    database.session.add(nome_acao_secundaria)
    database.session.flush()

    ciclo_secundario = CicloAcaoAgapeFactory(
        fk_acao_agape_id=nome_acao_secundaria.id,
        fk_endereco_id=endereco_ciclo_secundario.id,
    )
    database.session.add(ciclo_secundario)
    database.session.flush()

    doacao_secundaria = DoacaoAgapeFactory(fk_familia_agape_id=familia.id)
    database.session.add(doacao_secundaria)
    database.session.flush()

    item_estoque_sec = EstoqueAgapeFactory(item='Item Secundário 1')
    database.session.add(item_estoque_sec)
    database.session.flush()
    item_instancia_sec = ItemInstanciaAgapeFactory(
        fk_instancia_acao_agape_id=ciclo_secundario.id,
        fk_estoque_agape_id=item_estoque_sec.id,
        quantidade=15,
    )
    database.session.add(item_instancia_sec)
    database.session.flush()
    ItemDoacaoAgapeFactory(
        fk_doacao_agape_id=doacao_secundaria.id,
        fk_item_instancia_agape_id=item_instancia_sec.id,
        quantidade=7,
    )

    database.session.commit()
    itens_esperados_principal.sort(key=lambda x: x['nome_item'])
    return ciclo_principal.id, doacao_principal.id, itens_esperados_principal


@pytest.fixture
def seed_doacao_em_ciclo_sem_itens(
    seed_familia_com_endereco,
    seed_nome_acao_agape,
):
    familia, _ = seed_familia_com_endereco

    endereco_ciclo_principal = EnderecoFactory()
    database.session.add(endereco_ciclo_principal)
    database.session.flush()

    nome_acao_principal = seed_nome_acao_agape
    ciclo_principal = CicloAcaoAgapeFactory(
        fk_acao_agape_id=nome_acao_principal.id,
        fk_endereco_id=endereco_ciclo_principal.id,
    )
    database.session.add(ciclo_principal)
    database.session.flush()

    doacao_principal = DoacaoAgapeFactory(fk_familia_agape_id=familia.id)
    database.session.add(doacao_principal)
    database.session.flush()

    endereco_ciclo_secundario = EnderecoFactory(cidade='Outra Cidade')
    database.session.add(endereco_ciclo_secundario)
    database.session.flush()

    nome_acao_secundaria = NomeAcaoAgapeFactory(nome='Ação Secundária')
    database.session.add(nome_acao_secundaria)
    database.session.flush()

    ciclo_secundario = CicloAcaoAgapeFactory(
        fk_acao_agape_id=nome_acao_secundaria.id,
        fk_endereco_id=endereco_ciclo_secundario.id,
    )
    database.session.add(ciclo_secundario)
    database.session.flush()

    doacao_secundaria = DoacaoAgapeFactory(fk_familia_agape_id=familia.id)
    database.session.add(doacao_secundaria)
    database.session.flush()

    database.session.commit()

    return ciclo_principal.id, doacao_principal.id
