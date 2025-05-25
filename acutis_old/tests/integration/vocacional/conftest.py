from datetime import datetime
from faker import Faker
import pytest
from builder import db
from models.vocacional.cadastro_vocacional import CadastroVocacional
from models.vocacional.etapa_vocacional import EtapaVocacional
from models.vocacional.ficha_vocacional import FichaVocacional
from models.vocacional.usuario_vocacional import UsuarioVocacional
from tests.factories import EnderecoFactory, EtapaVocacionalFactory, FichaVocacionalFactory, UsuarioVocacionalFactory

faker = Faker("pt_BR")

@pytest.fixture
def seed_pre_cadastro_vocacional_pendentes():
    registros = []

    for _ in range(10):
        new_pre_cadastro = UsuarioVocacionalFactory()
        db.session.add(new_pre_cadastro)
        db.session.flush()

        new_etapa = EtapaVocacionalFactory(fk_usuario_vocacional_id=new_pre_cadastro.id)

        db.session.add(new_etapa)
        db.session.commit()
        registros.append((new_pre_cadastro, new_etapa))

    return registros


@pytest.fixture
def seed_pre_cadastro_vocacional_aproved():
    
    new_pre_cadastro = UsuarioVocacionalFactory()

    db.session.add(new_pre_cadastro)
    db.session.flush()

    new_etapa = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa="pre_cadastro",
        status="aprovado",
    )

    db.session.add(new_etapa)
    db.session.commit()

    return new_pre_cadastro, new_etapa

@pytest.fixture
def seed_pre_cadastro_vocacional_reproved():
    new_pre_cadastro = UsuarioVocacionalFactory()

    db.session.add(new_pre_cadastro)
    db.session.flush()

    new_etapa = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa="pre_cadastro",
        status="reprovado",
    )

    db.session.add(new_etapa)
    db.session.commit()

    return new_pre_cadastro, new_etapa

@pytest.fixture
def seed_pre_cadastro_vocacional_desistencia():

    new_pre_cadastro = UsuarioVocacionalFactory()

    db.session.add(new_pre_cadastro)
    db.session.flush()

    new_etapa = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa="pre_cadastro",
        status="desistencia",
    )

    db.session.add(new_etapa)
    db.session.commit()

    return new_pre_cadastro, new_etapa


@pytest.fixture
def seed_cadastro_vocacional_pendente():
    new_pre_cadastro = UsuarioVocacionalFactory()

    db.session.add(new_pre_cadastro)
    db.session.flush()
    
    new_endereco = EnderecoFactory()
    
    db.session.add(new_endereco)
    db.session.flush()
    
    
    new_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa="pre_cadastro",
        status="aprovado",
    )

    db.session.add(new_etapa_pre_cadastro)
    db.session.flush()
    
    
    new_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id = new_pre_cadastro.id,
        fk_endereco_id = new_endereco.id,
        data_nascimento= datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade="20994073046"
    )
    
    db.session.add(new_cadastro_vocacional)
    db.session.flush()
    
    new_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa="cadastro",
        status="pendente",
    )
    
    db.session.add(new_etapa_cadastro)
    
    db.session.commit()

    return  new_cadastro_vocacional


@pytest.fixture
def seed_cadastro_vocacional_aprovado():
    
    new_pre_cadastro = UsuarioVocacionalFactory()

    db.session.add(new_pre_cadastro)
    db.session.flush()
    
    
    new_etapa_pre_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa="pre_cadastro",
        status="aprovado",
    )

    db.session.add(new_etapa_pre_cadastro)
    db.session.flush()
    
    new_endereco = EnderecoFactory()
    
    db.session.add(new_endereco)
    db.session.flush()
    
    
    new_cadastro_vocacional = CadastroVocacional(
        fk_usuario_vocacional_id = new_pre_cadastro.id,
        fk_endereco_id = new_endereco.id,
        data_nascimento= datetime.strptime(faker.date(), '%Y-%m-%d').date(),
        documento_identidade=faker.random_int(min=12)
    )
    
    db.session.add(new_cadastro_vocacional)
    db.session.flush()
    
    new_etapa_cadastro = EtapaVocacional(
        fk_usuario_vocacional_id=new_pre_cadastro.id,
        etapa="cadastro",
        status="aprovado",
    )
    
    db.session.add(new_etapa_cadastro)
    
    db.session.commit()

    return new_pre_cadastro, new_cadastro_vocacional


@pytest.fixture
def seed_ficha_vocacional(seed_cadastro_vocacional_aprovado):

    pre_cadastro, cadastro_vocacional = seed_cadastro_vocacional_aprovado
    
    new_ficha_vocacional = FichaVocacionalFactory(
        fk_usuario_vocacional_id=pre_cadastro.id  
    )

    db.session.add(new_ficha_vocacional)
    db.session.flush()
    
    new_etapa_ficha_vocacional = EtapaVocacional(
        fk_usuario_vocacional_id=cadastro_vocacional.id,
        etapa="ficha_vocacional",
        status="pendente",
    )
    
    db.session.add(new_etapa_ficha_vocacional)
    
    db.session.commit()
    
    return pre_cadastro, cadastro_vocacional, new_ficha_vocacional


@pytest.fixture
def seed_vocacionais_reprovados():
    
    usuarios = []
    etapas = []
    for _ in range(5):
        new_pre_cadastro = UsuarioVocacionalFactory()
        db.session.add(new_pre_cadastro)
        db.session.flush()
        
        new_etapa = EtapaVocacional(
            fk_usuario_vocacional_id=new_pre_cadastro.id,
            etapa="pre_cadastro",
            status="reprovado",
            justificativa="fsfs",
            responsavel=1
        )
        usuarios.append(new_pre_cadastro)
        etapas.append(new_etapa)
        
        db.session.add(new_etapa)
        db.session.commit()
        
        
    return usuarios, etapas

