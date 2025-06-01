from datetime import datetime, timezone
from random import choice

import factory
from faker import Faker

from acutis_api.application.utils.funcoes_auxiliares import (
    valida_cpf_cnpj,
)
from acutis_api.domain.entities.acao_agape import AcaoAgape
from acutis_api.domain.entities.audiencia_live import AudienciaLive
from acutis_api.domain.entities.benfeitor import Benfeitor
from acutis_api.domain.entities.campanha import Campanha, ObjetivosCampanhaEnum
from acutis_api.domain.entities.campanha_doacao import CampanhaDoacao
from acutis_api.domain.entities.campo_adicional import (
    CampoAdicional,
    TiposCampoEnum,
)
from acutis_api.domain.entities.cargo_oficial import CargosOficiais
from acutis_api.domain.entities.doacao import Doacao
from acutis_api.domain.entities.doacao_agape import DoacaoAgape
from acutis_api.domain.entities.endereco import Endereco
from acutis_api.domain.entities.estoque_agape import EstoqueAgape
from acutis_api.domain.entities.etapa_vocacional import (
    EtapaVocacional,
    PassosVocacionalEnum,
    PassosVocacionalStatusEnum,
)
from acutis_api.domain.entities.familia_agape import FamiliaAgape
from acutis_api.domain.entities.ficha_vocacional import FichaVocacional
from acutis_api.domain.entities.instancia_acao_agape import (
    AbrangenciaInstanciaAcaoAgapeEnum,
    InstanciaAcaoAgape,
)
from acutis_api.domain.entities.item_doacao_agape import ItemDoacaoAgape
from acutis_api.domain.entities.item_instancia_agape import ItemInstanciaAgape
from acutis_api.domain.entities.landing_page import LandingPage
from acutis_api.domain.entities.lead import Lead, OrigemCadastroEnum
from acutis_api.domain.entities.lead_campanha import LeadCampanha
from acutis_api.domain.entities.live import Live
from acutis_api.domain.entities.live_avulsa import LiveAvulsa
from acutis_api.domain.entities.live_recorrente import LiveRecorrente
from acutis_api.domain.entities.membro import Membro, SexoEnum
from acutis_api.domain.entities.membro_agape import MembroAgape
from acutis_api.domain.entities.metadado_lead import MetadadoLead
from acutis_api.domain.entities.oficial import Oficial
from acutis_api.domain.entities.pagamento_doacao import (
    FormaPagamentoEnum,
    GatewayPagamentoEnum,
    PagamentoDoacao,
)
from acutis_api.domain.entities.perfil import Perfil
from acutis_api.domain.entities.permissao_lead import PermissaoLead
from acutis_api.domain.entities.processamento_doacao import (
    ProcessamentoDoacao,
    StatusProcessamentoEnum,
)
from acutis_api.domain.entities.usuario_vocacional import UsuarioVocacional

faker = Faker(locale='pt-BR')
faker.word()


class LeadFactory(factory.Factory):
    class Meta:
        model = Lead

    nome = factory.Faker('name', locale='pt-BR')
    email = factory.Faker('email', domain='headers.com.br')
    telefone = factory.Faker('cellphone_number', locale='pt-BR')
    pais = factory.Faker('country')
    origem_cadastro = factory.Faker(
        'random_element', elements=OrigemCadastroEnum
    )
    ultimo_acesso = None
    status = False

    @factory.post_generation
    def criar_senha(obj, create, extracted, **kwargs):
        if create:
            obj.senha = '#Teste;@123'


class EnderecoFactory(factory.Factory):
    class Meta:
        model = Endereco

    codigo_postal = factory.Faker('postcode', locale='pt-BR')
    tipo_logradouro = factory.Faker('word')
    logradouro = factory.Faker('street_name')
    numero = factory.Faker('building_number')
    complemento = factory.Faker('secondary_address')
    bairro = factory.Faker('city_suffix')
    cidade = factory.Faker('city')
    estado = factory.Faker('state')
    pais = factory.Faker('country')


class MembroFactory(factory.Factory):
    class Meta:
        model = Membro

    fk_lead_id = factory.LazyAttribute(lambda _: LeadFactory().id)
    fk_endereco_id = factory.LazyAttribute(lambda _: EnderecoFactory().id)
    fk_benfeitor_id = None
    nome_social = factory.Faker('name')
    data_nascimento = factory.Faker('date_of_birth')
    numero_documento = factory.Faker('cpf', locale='pt_BR')
    sexo = factory.Faker('random_element', elements=SexoEnum)
    foto = None


class CampanhasFactory(factory.Factory):
    class Meta:
        model = Campanha

    objetivo = factory.LazyAttribute(
        lambda _: choice(list(ObjetivosCampanhaEnum))
    )
    nome = factory.Faker('sentence', nb_words=4, locale='pt_BR')
    publica = factory.Faker('boolean')
    ativa = factory.Faker('boolean')
    meta = factory.Faker(
        'pyfloat', positive=True, min_value=1000, max_value=100000
    )
    capa = None
    chave_pix = factory.Faker('uuid4')
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)


class LandingPageFactory(factory.Factory):
    class Meta:
        model = LandingPage

    fk_campanha_id = factory.LazyFunction(lambda: CampanhaFactory().id)
    conteudo = factory.Faker('text', max_nb_chars=500, locale='pt_BR')
    shlink = factory.Faker('url')
    estrutura_json = factory.Faker('text', max_nb_chars=500, locale='pt_BR')


class CampanhaFactory(factory.Factory):
    class Meta:
        model = Campanha

    objetivo = factory.Faker('random_element', elements=ObjetivosCampanhaEnum)
    nome = factory.Faker('sentence', nb_words=4, locale='pt_BR')
    publica = True
    ativa = True
    meta = factory.Faker(
        'pyfloat', positive=True, min_value=1000, max_value=100000
    )
    capa = None
    chave_pix = factory.Faker('uuid4')
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)
    fk_cargo_oficial_id = None
    superior_obrigatorio = None


class CampanhaDoacaoFactory(factory.Factory):
    class Meta:
        model = CampanhaDoacao

    chave_pix = factory.Faker('uuid4')
    fk_campanha_id = factory.LazyAttribute(lambda _: CampanhaFactory().id)


class LeadCampanhaFactory(factory.Factory):
    class Meta:
        model = LeadCampanha

    fk_lead_id = factory.LazyAttribute(lambda _: LeadFactory().id)
    fk_campanha_id = factory.LazyAttribute(lambda _: CampanhaFactory().id)


class CampoAdicionalFactory(factory.Factory):
    class Meta:
        model = CampoAdicional

    fk_campanha_id = factory.LazyAttribute(lambda _: CampanhaFactory().id)
    nome_campo = factory.Faker('name')
    tipo_campo = factory.Faker('random_element', elements=TiposCampoEnum)
    obrigatorio = True


class MetadadoLeadFactory(factory.Factory):
    class Meta:
        model = MetadadoLead

    fk_lead_id = factory.LazyAttribute(lambda _: LeadFactory().id)
    fk_campo_adicional_id = factory.LazyAttribute(
        lambda _: CampoAdicionalFactory().id
    )
    valor_campo = None


class UsuarioVocacionalFactory(factory.Factory):
    class Meta:
        model = UsuarioVocacional

    nome = factory.Faker('name', locale='pt_BR')
    email = factory.Faker('email', locale='pt_BR')
    telefone = factory.Faker('phone_number', locale='pt_BR')
    genero = factory.Faker(
        'random_element', elements=('masculino', 'feminino')
    )
    pais = factory.Faker('country', locale='pt_BR')


class EtapaVocacionalFactory(factory.Factory):
    class Meta:
        model = EtapaVocacional

    fk_usuario_vocacional_id = factory.LazyAttribute(
        lambda o: UsuarioVocacionalFactory().id
    )
    etapa = PassosVocacionalEnum.pre_cadastro
    status = PassosVocacionalStatusEnum.pendente
    justificativa = None
    fk_responsavel_id = None


class FichaVocacionalFactory(factory.Factory):
    class Meta:
        model = FichaVocacional

    fk_usuario_vocacional_id = factory.LazyAttribute(
        lambda o: UsuarioVocacionalFactory().id
    )
    motivacao_instituto = factory.Faker('text', max_nb_chars=200)
    motivacao_admissao_vocacional = factory.Faker('text', max_nb_chars=200)
    referencia_conhecimento_instituto = factory.Faker('text', max_nb_chars=200)
    identificacao_instituto = factory.Faker('text', max_nb_chars=200)
    foto_vocacional = factory.Faker('file_name', extension='jpg')
    seminario_realizado_em = factory.Faker(
        'date_between', start_date='-5y', end_date='today'
    )
    testemunho_conversao = factory.Faker('text', max_nb_chars=500)
    escolaridade = factory.Faker(
        'random_element',
        elements=('Ensino Médio', 'Ensino Superior', 'Pós-Graduação'),
    )
    profissao = factory.Faker('job')
    cursos = factory.Faker('text', max_nb_chars=100)
    rotina_diaria = factory.Faker('text', max_nb_chars=200)
    aceitacao_familiar = factory.Faker('text', max_nb_chars=200)
    estado_civil = 'Solteiro(a)'
    motivo_divorcio = None
    deixou_religiao_anterior_em = factory.Faker(
        'date_between', start_date='-10y', end_date='today'
    )
    remedio_controlado_inicio = factory.Faker(
        'date_between', start_date='-5y', end_date='today'
    )
    remedio_controlado_termino = factory.Faker(
        'date_between', start_date='-5y', end_date='today'
    )
    descricao_problema_saude = factory.Faker('text', max_nb_chars=300)


class CargosOficiaisFactory(factory.Factory):
    class Meta:
        model = CargosOficiais

    nome_cargo = factory.Faker('name')
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)
    fk_cargo_superior_id = None
    atualizado_por = None


class CargoOficialGeneralFactory(factory.Factory):
    class Meta:
        model = CargosOficiais

    nome_cargo = 'General'
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)
    atualizado_por = None
    fk_cargo_superior_id = factory.LazyAttribute(
        lambda _: CargoOficialMarechalFactory().id
    )


class CargoOficialMarechalFactory(factory.Factory):
    class Meta:
        model = CargosOficiais

    nome_cargo = 'Marechal'
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)
    fk_cargo_superior_id = None
    atualizado_por = None


class MembroOficialFactory(factory.Factory):
    class Meta:
        model = Oficial

    fk_membro_id = factory.LazyAttribute(lambda _: MembroFactory().id)
    fk_superior_id = factory.LazyAttribute(lambda _: MembroFactory().id)
    fk_cargo_oficial_id = factory.LazyAttribute(
        lambda _: CargosOficiaisFactory().id
    )
    status = factory.LazyAttribute(lambda _: 'aprovado')
    atualizado_por = None


class CampanhaMembroOficialFactory(factory.Factory):
    class Meta:
        model = Campanha

    objetivo = ObjetivosCampanhaEnum.oficiais
    nome = factory.Faker('sentence', nb_words=4, locale='pt_BR')
    publica = True
    ativa = True
    meta = factory.Faker(
        'pyfloat', positive=True, min_value=1000, max_value=100000
    )
    capa = None
    chave_pix = None
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)
    fk_cargo_oficial_id = factory.LazyAttribute(
        lambda _: CargosOficiaisFactory().id
    )
    superior_obrigatorio = None


class BenfeitorFactory(factory.Factory):
    class Meta:
        model = Benfeitor

    numero_documento = factory.Faker('cpf', locale='pt_BR')
    nome = factory.Faker('name', locale='pt_BR')


class DoacaoFactory(factory.Factory):
    class Meta:
        model = Doacao

    fk_benfeitor_id = factory.LazyAttribute(lambda _: BenfeitorFactory().id)
    fk_campanha_doacao_id = factory.LazyAttribute(
        lambda _: CampanhaDoacaoFactory().id
    )
    cancelado_em = None
    cancelado_por = None
    contabilizar = True


class PagamentoDoacaoFactory(factory.Factory):
    class Meta:
        model = PagamentoDoacao

    fk_doacao_id = factory.LazyAttribute(lambda _: DoacaoFactory().id)
    valor = 10.0
    recorrente = False
    forma_pagamento = FormaPagamentoEnum.credito
    codigo_ordem_pagamento = None
    anonimo = False
    gateway = GatewayPagamentoEnum.maxipago
    ativo = True


class ProcessamentoDoacaoFactory(factory.Factory):
    class Meta:
        model = ProcessamentoDoacao

    fk_pagamento_doacao_id = factory.LazyAttribute(
        lambda _: PagamentoDoacaoFactory().id
    )
    forma_pagamento = FormaPagamentoEnum.credito
    processado_em = datetime.now()
    codigo_referencia = None
    codigo_transacao = None
    codigo_comprovante = None
    nosso_numero = None
    status = StatusProcessamentoEnum.pago


class NomeAcaoAgapeFactory(factory.Factory):
    class Meta:
        model = AcaoAgape

    nome = factory.Faker('name', locale='pt-BR')


class CicloAcaoAgapeFactory(factory.Factory):
    class Meta:
        model = InstanciaAcaoAgape

    data_inicio = None
    data_termino = None
    abrangencia = factory.Faker(
        'random_element', elements=AbrangenciaInstanciaAcaoAgapeEnum
    )


class EstoqueAgapeFactory(factory.Factory):
    class Meta:
        model = EstoqueAgape

    item = factory.Faker('name', locale='pt-BR')
    quantidade = factory.Faker('random_int')


class LiveFactory(factory.Factory):
    class Meta:
        model = Live

    tag = factory.LazyFunction(faker.word)
    fk_campanha_id = factory.LazyAttribute(lambda _: CampanhaFactory().id)
    rede_social = factory.LazyFunction(
        lambda: choice(['youtube', 'instagram', 'facebook'])
    )
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)


class LiveAvulsaFactory(factory.Factory):
    class Meta:
        model = LiveAvulsa

    fk_live_id = factory.LazyAttribute(lambda _: LiveFactory().id)
    data_hora_inicio = datetime.now()
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)


class LiveRecorrenteFactory(factory.Factory):
    class Meta:
        model = LiveRecorrente

    dia_semana = factory.LazyFunction(
        lambda: choice([
            'segunda',
            'terça',
            'quarta',
            'quinta',
            'sexta',
            'sábado',
            'domingo',
        ])
    )
    hora_inicio = factory.LazyFunction(lambda _: faker.time_object())
    fk_live_id = factory.LazyAttribute(lambda _: LiveFactory().id)
    criado_por = factory.LazyAttribute(lambda _: MembroFactory().id)


class AudienciaFactory(factory.Factory):
    class Meta:
        model = AudienciaLive

    fk_live_id = factory.LazyAttribute(lambda _: LiveFactory().id)
    titulo = factory.LazyFunction(
        lambda: f'Live - {faker.sentence(nb_words=2)}'
    )
    audiencia = factory.Faker('random_int', min_value=0, max=500)
    data_hora_registro = factory.LazyFunction(
        lambda: datetime.now(timezone.utc)
    )


class PerfilFactory(factory.Factory):
    class Meta:
        model = Perfil

    nome = factory.Faker('job', locale='pt-BR')
    status = True
    super_perfil = False
    permissoes_lead = factory.List([])
    permissoes_menu = factory.List([])

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        kwargs.setdefault('permissoes_lead', [])
        kwargs.setdefault('permissoes_menu', [])
        return model_class(*args, **kwargs)


class PermissaoLeadFactory(factory.Factory):
    class Meta:
        model = PermissaoLead


class FamiliaAgapeFactory(factory.Factory):
    class Meta:
        model = FamiliaAgape

    status = True
    deletado_em = None
    comprovante_residencia = factory.Faker('file_name', extension='jpg')
    nome_familia = factory.Faker('name', locale='pt-BR')
    observacao = factory.Faker('name', locale='pt-BR')


class MembroAgapeFactory(factory.Factory):
    class Meta:
        model = MembroAgape

    fk_familia_agape_id = factory.LazyAttribute(
        lambda _: FamiliaAgapeFactory().id
    )
    responsavel = True
    nome = factory.Faker('name', locale='pt-BR')
    email = factory.Faker('email', locale='pt-BR')
    telefone = factory.Faker('phone_number', locale='pt-BR')
    cpf = factory.LazyFunction(
        lambda: valida_cpf_cnpj(faker.cpf(), tipo_documento='cpf')
    )
    data_nascimento = factory.Faker(
        'date_of_birth', minimum_age=1, maximum_age=100
    )
    funcao_familiar = factory.Faker(
        'random_element',
        elements=['Pai', 'Mãe', 'Filho(a)', 'Avô(ó)', 'Neto(a)'],
    )
    escolaridade = factory.Faker(
        'random_element',
        elements=[
            'Analfabeto',
            'Ensino Fundamental Incompleto',
            'Ensino Fundamental Completo',
            'Ensino Médio Incompleto',
            'Ensino Médio Completo',
            'Superior Incompleto',
            'Superior Completo',
        ],
    )
    ocupacao = factory.Faker('job', locale='pt-BR')
    renda = factory.Faker(
        'pydecimal',
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=1000,
        max_value=10000,
    )
    beneficiario_assistencial = factory.Faker('boolean')
    foto_documento = factory.Faker('file_name', extension='jpg')


class DoacaoAgapeFactory(factory.Factory):
    class Meta:
        model = DoacaoAgape


class ItemInstanciaAgapeFactory(factory.Factory):
    class Meta:
        model = ItemInstanciaAgape

    quantidade = factory.Faker('random_int')


class ItemDoacaoAgapeFactory(factory.Factory):
    class Meta:
        model = ItemDoacaoAgape

    quantidade = factory.Faker('random_int')
