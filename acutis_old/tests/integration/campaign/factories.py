import factory
from models.campanha import Campanha
from faker import Faker

fake = Faker()

class CampaignFactory(factory.Factory):
    class Meta:
        model = Campanha
    fk_empresa_id = factory.Faker("random_int", min=1, max=100)
    titulo = "titulo bom demaise"
    descricao = factory.Faker("text", locale="pt_BR")
    
    data_inicio = factory.LazyFunction(fake.date_object)
    data_fim = factory.LazyFunction(fake.date_object)
    data_prorrogacao = factory.LazyFunction(fake.date_object)
    data_fechamento_campanha = factory.LazyFunction(fake.date_object)
    
    data_criacao = factory.LazyFunction(fake.date_time)
    data_alteracao = factory.LazyFunction(fake.date_time)
    deleted_at = None

    valor_meta = factory.Faker("random_int", min=1, max=1000)
    prorrogado = factory.Faker("random_int", min=1, max=100)
    valor_total_atingido = factory.Faker("random_int", min=1, max=1000)
    status = True
    publica = True
    filename = factory.Faker("name")
    chave_pix = factory.Faker("name")
    usuario_criacao = factory.Faker("random_int", min=1, max=100)
    usuario_alteracao = factory.Faker("random_int", min=1, max=100)
    duracao = factory.Faker("name")
    objetivo = "cadastro"
    cadastros_meta = factory.Faker("random_int", min=1, max=100)
    preenchimento_foto = factory.Faker("boolean")
    label_foto = factory.Faker("name")
    zone = factory.Faker("name")
    zone_id = factory.Faker("name")
    contabilizar_doacoes = factory.Faker("boolean")
