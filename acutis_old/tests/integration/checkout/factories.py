import factory

from models.campanha import Campanha
from models.pedido import Pedido
from models.clifor import Clifor
from models.processamento_pedido import ProcessamentoPedido
from utils.functions import get_current_time
from models.usuario import Usuario


class UsuarioFactory(factory.Factory):

    class Meta:
        model = Usuario

    nome = factory.Faker("name", locale="pt_BR")
    status = 1
    data_inicio = factory.LazyFunction(get_current_time)
    password_hash = "pbkdf2:sha256:600000$sxgBUkGVCn0qDNmZ$f8962544c7e7d1a6a697c92c8ef61af428a65898841797fde494033150251580"
    data_ultimo_acesso = factory.LazyFunction(get_current_time)
    email = factory.Faker("email", locale="pt_BR", domain="gmail.com")
    bloqueado = 0
    data_criacao = factory.LazyFunction(get_current_time)
    data_alteracao = factory.LazyFunction(get_current_time)
    avatar = "3eecdc9b-9d63-425a-8e55-7682ea73af88.jpeg"
    country = factory.Faker("country", locale="pt_BR")


class CliforFactory(factory.Factory):

    class Meta:
        model = Clifor

    fk_empresa_id = 1
    fk_usuario_id = factory.LazyFunction(lambda a: UsuarioFactory().id)
    tipo_clifor = "f"
    nome = factory.LazyFunction(lambda: UsuarioFactory().nome)
    cpf_cnpj = factory.Faker("cpf", locale="pt_BR")
    telefone1 = factory.Faker("phone_number", locale="pt_BR")
    email = factory.Faker("email", locale="pt_BR")
    status = 1
    data_nascimento = factory.Faker("date_of_birth")
    sexo = "masculino"
    data_criacao = factory.LazyFunction(get_current_time)
    usuario_criacao = 0


class CampanhaFactory(factory.Factory):
    class Meta:
        model = Campanha

    titulo = "titulo"
    descricao = factory.Faker("text", max_nb_chars=40)
    status = 1
    filename = "1642552024021965d3af3f0cd18.png"
    data_criacao = factory.LazyFunction(get_current_time)
    usuario_criacao = 1
    data_alteracao = factory.LazyFunction(get_current_time)
    usuario_alteracao = 30559
    chave_pix = "manda10"
    publica = 1
    duracao = "permanente"
    objetivo = "doacao"
    preenchimento_foto = 0
    cadastros_meta = 0
    valor_meta = 0
    contabilizar_doacoes = 1


class PedidoRecorrenteFactory(factory.Factory):
    class Meta:
        model = Pedido
        
    fk_empresa_id = 1
    fk_clifor_id = factory.LazyFunction(lambda a: CliforFactory().id)
    fk_campanha_id = factory.LazyFunction(lambda a: CampanhaFactory().id)
    usuario_criacao = factory.LazyFunction(lambda a: UsuarioFactory().id)
    fk_forma_pagamento_id = factory.Faker('random_element', elements=('1', '2', '3'))
    data_pedido = factory.LazyFunction(get_current_time)
    periodicidade = 2
    status_pedido = 1
    valor_total_pedido = factory.Faker("random_number", locale="pt_BR")
    anonimo = 0
    recorrencia_ativa = 1
    contabilizar_doacao = 1
    fk_gateway_pagamento_id = 1
    
class PedidoRecorrenteCanceladoFactory(factory.Factory):
    class Meta:
        model = Pedido
        
    fk_empresa_id = 1
    fk_clifor_id = factory.LazyFunction(lambda a: CliforFactory().id)
    fk_campanha_id = factory.LazyFunction(lambda a: CampanhaFactory().id)
    usuario_criacao = factory.LazyFunction(lambda a: UsuarioFactory().id)
    fk_forma_pagamento_id = factory.Faker('random_element', elements=('1', '2', '3'))
    data_pedido = factory.LazyFunction(get_current_time)
    periodicidade = 2
    status_pedido = 2
    valor_total_pedido = factory.Faker("random_number", locale="pt_BR")
    anonimo = 0
    recorrencia_ativa = False
    cancelada_por = factory.LazyFunction(lambda: UsuarioFactory().id)
    cancelada_em = factory.LazyFunction(get_current_time)
    contabilizar_doacao = 1
    fk_gateway_pagamento_id = 1


class ProcessamentoPedidoFactory(factory.Factory):
    class Meta:
        model = ProcessamentoPedido

    fk_empresa_id = 1
    fk_forma_pagamento_id = factory.Faker("random_element", elements=[1, 2, 3])
    data_processamento = factory.LazyFunction(get_current_time)
    valor = "0.08"
    status_processamento = factory.Faker("random_element", elements=[0, 1, 2, 3])
    id_transacao_gateway = "testeapenasteste"
    transaction_id = "temnao123123321"
    data_criacao = factory.LazyFunction(get_current_time)
    fk_pedido_id = factory.LazyFunction(lambda a: PedidoRecorrenteFactory().id)
    usuario_criacao = factory.LazyFunction(lambda: UsuarioFactory().id)
    fk_clifor_id = factory.LazyFunction(lambda a: CliforFactory().id)

