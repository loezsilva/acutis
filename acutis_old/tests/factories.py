import factory
from models.actions_leads import ActionsLeads
from models.agape.acao_agape import AcaoAgape
from models.agape.aquisicao_agape import AquisicaoAgape
from models.agape.doacao_agape import DoacaoAgape
from models.agape.estoque_agape import EstoqueAgape
from models.agape.familia_agape import FamiliaAgape
from models.agape.foto_familia_agape import FotoFamiliaAgape
from models.agape.historico_movimentacao_agape import (
    HistoricoMovimentacaoAgape,
    TipoMovimentacaoEnum,
)
from models.agape.instancia_acao_agape import (
    AbrangenciaInstanciaAcaoAgapeEnum,
    InstanciaAcaoAgape,
    StatusAcaoAgapeEnum,
)
from models.agape.item_doacao_agape import ItemDoacaoAgape
from models.agape.item_instancia_agape import ItemInstanciaAgape
from models.agape.membro_agape import MembroAgape
from models.agape.recibo_agape import ReciboAgape
from models.endereco import Endereco
from models.usuario import Usuario
from models.users_imports import UsersImports
from models.vocacional.etapa_vocacional import EtapaVocacional
from models.vocacional.ficha_vocacional import FichaVocacional
from models.vocacional.usuario_vocacional import UsuarioVocacional
from utils.functions import get_current_time

class DoacaoAgapeFactory(factory.Factory):
    class Meta:
        model = DoacaoAgape

    fk_familia_agape_id = factory.LazyAttribute(
        lambda _: FamiliaAgapeFactory().id
    )
    updated_at = factory.LazyFunction(get_current_time)


class EnderecoFactory(factory.Factory):
    class Meta:
        model = Endereco

    rua = factory.Faker("street_name")
    numero = factory.Faker("building_number")
    complemento = factory.Faker("secondary_address")
    ponto_referencia = factory.Faker("sentence", nb_words=3)
    bairro = factory.Faker("city_suffix")
    cidade = factory.Faker("city")
    estado = factory.Faker("state")
    cep = factory.Faker("postcode")
    obriga_atualizar_endereco = False
    ultima_atualizacao_endereco = factory.LazyFunction(get_current_time)
    data_criacao = factory.LazyFunction(get_current_time)
    usuario_criacao = factory.Faker("random_int", min=1, max=100)
    detalhe_estrangeiro = factory.Faker("text")
    pais_origem = factory.Faker("country")
    latitude = factory.Faker("latitude")
    longitude = factory.Faker("longitude")
    latitude_nordeste = factory.Faker("latitude")
    longitude_nordeste = factory.Faker("longitude")
    latitude_sudoeste = factory.Faker("latitude")
    longitude_sudoeste = factory.Faker("longitude")


class EstoqueAgapeFactory(factory.Factory):
    class Meta:
        model = EstoqueAgape

    item = factory.Faker("name")
    quantidade = factory.Faker("random_int", min=1, max=1000)


class FamiliaAgapeFactory(factory.Factory):
    class Meta:
        model = FamiliaAgape

    fk_endereco_id = factory.LazyAttribute(lambda _: EnderecoFactory().id)
    nome_familia = factory.Faker("last_name")
    status = factory.Faker("random_element", elements=[True, False])
    updated_at = factory.LazyFunction(get_current_time)
    deleted_at = None
    cadastrada_por = factory.LazyAttribute(lambda _: UsuarioFactory().id)


class FotoFamiliaAgapeFactory(factory.Factory):
    class Meta:
        model = FotoFamiliaAgape

    fk_familia_agape_id = factory.LazyAttribute(lambda _: FamiliaAgapeFactory().id)
    foto = factory.Faker('word', locale='pt_BR')


class MembroAgapeFactory(factory.Factory):
    class Meta:
        model = MembroAgape

    fk_familia_agape_id = factory.LazyAttribute(
        lambda _: FamiliaAgapeFactory().id
    )
    responsavel = factory.Faker("boolean")
    nome = factory.Faker("name", locale="pt_BR")
    email = factory.Faker("email", domain="headers.com.br", locale="pt_BR")
    telefone = factory.Faker("cellphone_number", locale="pt_BR")
    cpf = factory.Faker("cpf", locale="pt_BR")
    data_nascimento = factory.Faker("date_of_birth")
    funcao_familiar = factory.Faker("sentence", nb_words=1, locale="pt_BR")
    escolaridade = factory.Faker("word", locale="pt_BR")
    ocupacao = factory.Faker("job", locale="pt_BR")
    renda = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True
    )
    foto_documento = factory.Faker("word", locale="pt_BR")
    beneficiario_assistencial = factory.Faker("random_element", elements=[True, False])


class AcaoAgapeFactory(factory.Factory):
    class Meta:
        model = AcaoAgape

    nome = factory.Faker("name")
    updated_at = factory.LazyFunction(get_current_time)


class InstanciaAcaoAgapeFactory(factory.Factory):
    class Meta:
        model = InstanciaAcaoAgape

    fk_endereco_id = factory.LazyAttribute(lambda _: EnderecoFactory().id)
    fk_acao_agape_id = factory.LazyAttribute(lambda _: AcaoAgapeFactory().id)
    status = StatusAcaoAgapeEnum.nao_iniciado
    abrangencia = factory.Faker(
        "random_element", elements=AbrangenciaInstanciaAcaoAgapeEnum
    )
    data_inicio = factory.Faker("date_time")
    data_termino = factory.Faker("date_time")
    updated_at = factory.LazyFunction(get_current_time)


class EstoqueAgapeFactory(factory.Factory):
    class Meta:
        model = EstoqueAgape

    item = factory.Faker("name")
    quantidade = factory.Faker("random_int", min=1, max=1000)
    updated_at = factory.LazyFunction(get_current_time)


class ItemInstanciaAgapeFactory(factory.Factory):
    class Meta:
        model = ItemInstanciaAgape

    fk_instancia_acao_agape_id = factory.LazyAttribute(
        lambda _: InstanciaAcaoAgapeFactory().id
    )
    fk_estoque_agape_id = factory.LazyAttribute(
        lambda _: EstoqueAgapeFactory().id
    )
    quantidade = factory.Faker("random_int", min=1, max=1000)
    updated_at = factory.LazyFunction(get_current_time)


class ReciboAgapeFactory(factory.Factory):
    class Meta:
        model = ReciboAgape

    fk_doacao_agape_id = factory.LazyAttribute(
        lambda _: DoacaoAgapeFactory().id
    )
    recibo = factory.Faker("word", locale="pt_BR")
    updated_at = factory.LazyFunction(get_current_time)


class ItemDoacaoAgapeFactory(factory.Factory):
    class Meta:
        model = ItemDoacaoAgape

    fk_item_instancia_agape_id = factory.LazyAttribute(
        lambda _: ItemInstanciaAgapeFactory().id
    )
    fk_doacao_agape_id = factory.LazyAttribute(
        lambda _: DoacaoAgapeFactory().id
    )
    quantidade = factory.Faker("random_int", min=1, max=1000)
    updated_at = factory.LazyFunction(get_current_time)


class HistoricoMovimentacaoAgapeFactory(factory.Factory):
    class Meta:
        model = HistoricoMovimentacaoAgape

    fk_estoque_agape_id = factory.LazyAttribute(
        lambda _: EstoqueAgapeFactory().id
    )
    quantidade = factory.Faker("random_int", min=1, max=1000)
    tipo_movimentacao = factory.Faker(
        "random_element", elements=TipoMovimentacaoEnum
    )
    updated_at = factory.LazyFunction(get_current_time)


class AquisicaoAgapeFactory(factory.Factory):
    class Meta:
        model = AquisicaoAgape

    fk_estoque_agape_id = factory.LazyAttribute(
        lambda _: EstoqueAgapeFactory().id
    )
    quantidade = factory.Faker("random_int", min=1, max=1000)
    updated_at = factory.LazyFunction(get_current_time)


class AcaoLeadFactory(factory.Factory):
    class Meta:
        model = ActionsLeads

    nome = factory.Faker("name", locale="pt_BR")
    titulo = factory.Faker("name", locale="pt_BR")
    descricao = factory.Faker("text", locale="pt_BR")
    status = True
    preenchimento_foto = False


class LeadFactory(factory.Factory):
    class Meta:
        model = UsersImports

    nome = factory.Faker("name", locale="pt_BR")
    email = factory.Faker("email", locale="pt_BR", domain="gmail.com")
    data_criacao = factory.LazyFunction(get_current_time)
    phone = factory.Faker("phone_number", locale="pt_BR")
    origem_cadastro = factory.LazyAttribute(lambda _: AcaoLeadFactory().id)
    intencao = factory.Faker("text", locale="pt_BR")


class AcaoLeadFactory(factory.Factory):
    class Meta:
        model = ActionsLeads

    nome = factory.Faker("name", locale="pt_BR")
    titulo = factory.Faker("name", locale="pt_BR")
    descricao = factory.Faker("text", locale="pt_BR")
    status = True
    preenchimento_foto = False


class LeadFactory(factory.Factory):
    class Meta:
        model = UsersImports

    nome = factory.Faker("name", locale="pt_BR")
    email = factory.Faker("email", locale="pt_BR", domain="gmail.com")
    data_criacao = factory.LazyFunction(get_current_time)
    phone = factory.Faker("phone_number", locale="pt_BR")
    origem_cadastro = factory.LazyAttribute(lambda _: AcaoLeadFactory().id)
    intencao = factory.Faker("text", locale="pt_BR")


class UsuarioFactory(factory.Factory):
    class Meta:
        model = Usuario

    nome = factory.Faker("name", locale="pt_BR")
    nome_social = factory.Faker("name", locale="pt_BR")
    status = True
    data_inicio = factory.LazyFunction(get_current_time)
    obriga_atualizar_cadastro = False
    data_ultimo_acesso = factory.LazyFunction(get_current_time)
    email = factory.Faker("email", locale="pt_BR")
    bloqueado = False
    avatar = None
    campanha_origem = 1
    
    
class UsuarioVocacionalFactory(factory.Factory):
    class Meta:
        model = UsuarioVocacional

    nome = factory.Faker('name', locale='pt_BR')
    email = factory.Faker('email', locale='pt_BR')
    telefone = factory.Faker('phone_number', locale='pt_BR')
    genero = factory.Faker('random_element', elements=("masculino", "feminino"))
    pais = factory.Faker('country', locale='pt_BR')

class EtapaVocacionalFactory(factory.Factory):
    class Meta:
        model = EtapaVocacional

    fk_usuario_vocacional_id = factory.LazyAttribute(lambda o: UsuarioVocacionalFactory().id)
    etapa = "pre_cadastro"
    status = "pendente"
    
class FichaVocacionalFactory(factory.Factory):
    class Meta:
        model = FichaVocacional

    fk_usuario_vocacional_id = factory.LazyAttribute(lambda o: UsuarioVocacionalFactory().id)
    motivacao_instituto = factory.Faker('text', max_nb_chars=200)
    motivacao_admissao_vocacional = factory.Faker('text', max_nb_chars=200)
    referencia_conhecimento_instituto = factory.Faker('text', max_nb_chars=200)
    identificacao_instituto = factory.Faker('text', max_nb_chars=200)
    foto_vocacional = factory.Faker('file_name', extension="jpg")
    seminario_realizado_em = factory.Faker('date_between', start_date='-5y', end_date='today')
    testemunho_conversao = factory.Faker('text', max_nb_chars=500)
    escolaridade = factory.Faker('random_element', elements=("Ensino Médio", "Ensino Superior", "Pós-Graduação"))
    profissao = factory.Faker('job')
    cursos = factory.Faker('text', max_nb_chars=100)
    rotina_diaria = factory.Faker('text', max_nb_chars=200)
    aceitacao_familiar = factory.Faker('text', max_nb_chars=200)
    estado_civil = "Divorciado(a)"
    motivo_divorcio = factory.Faker('text', max_nb_chars=200)
    deixou_religiao_anterior_em = factory.Faker('date_between', start_date='-10y', end_date='today')
    remedio_controlado_inicio = factory.Faker('date_between', start_date='-5y', end_date='today')
    remedio_controlado_termino = factory.Faker('date_between', start_date='-5y', end_date='today')
    descricao_problema_saude = factory.Faker('text', max_nb_chars=300)